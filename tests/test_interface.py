"""Testes das janelas: entradas inválidas viram mensagem de erro, não exceção."""
import tkinter as tk

import pytest

from pystruct.ui import componentes, janela_laje_inclinada, janela_viga
from pystruct.ui.janela_escada import JanelaEscada
from pystruct.ui.janela_rampa import JanelaRampa
from pystruct.ui.janela_viga import JanelaViga


@pytest.fixture(scope="session")
def _tk():
    # uma única instância: criar várias seguidas falha de vez em quando no Windows
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tk indisponível neste ambiente")
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def raiz(_tk):
    yield _tk
    for filho in _tk.winfo_children():
        filho.destroy()


@pytest.fixture
def erros(monkeypatch):
    """Captura as mensagens que iriam para a caixa de erro."""
    mensagens = []
    capturar = lambda _janela, erro: mensagens.append(str(erro))
    monkeypatch.setattr(janela_laje_inclinada, "mostrar_erro", capturar)
    monkeypatch.setattr(janela_viga, "mostrar_erro", capturar)
    return mensagens


def preencher(**campos):
    for campo, valor in campos.items():
        campo.var.set(valor)


def test_campo_aceita_virgula_decimal(raiz):
    campo = componentes.Campo(raiz, 0, "fck (MPa):")
    campo.var.set(" 2,5 ")
    assert campo.valor() == 2.5


@pytest.mark.parametrize("texto", ["", "abc", "1,2,3"])
def test_campo_invalido_cita_o_rotulo(raiz, texto):
    campo = componentes.Campo(raiz, 0, "fck (MPa):")
    campo.var.set(texto)
    with pytest.raises(ValueError, match="fck"):
        campo.valor()


def preencher_rampa(janela, **alteracoes):
    valores = dict(v="0,3", h="1,2", espessura="20", c="2,5", ca="50", fck="25",
                   rev="1", bitola="10", bitola_sec="6,3")
    valores.update(alteracoes)
    for nome, valor in valores.items():
        getattr(janela, nome).var.set(valor)


def test_rampa_campo_vazio(raiz, erros):
    janela = JanelaRampa(raiz)
    preencher_rampa(janela, fck="")
    janela.calcular()
    assert len(erros) == 1 and "fck" in erros[0]
    assert janela.s_md.var.get() == ""


def test_rampa_horizontal_zero(raiz, erros):
    janela = JanelaRampa(raiz)
    preencher_rampa(janela, h="0")
    janela.calcular()
    assert erros == ["A distância horizontal deve ser maior que zero"]


def test_rampa_valida_preenche_resultados(raiz, erros):
    janela = JanelaRampa(raiz)
    preencher_rampa(janela)
    janela.calcular()
    assert erros == []
    assert janela.s_md.var.get() != ""
    assert janela.s_principal.var.get() != ""


def test_escada_piso_zero(raiz, erros):
    janela = JanelaEscada(raiz)
    for nome, valor in dict(h="3", espelho="17,5", piso="0", espessura="10", c="2,5", fck="25",
                            rev="1", bitola="10", bitola_sec="6,3").items():
        getattr(janela, nome).var.set(valor)
    janela.calcular()
    assert erros == ["O piso do degrau deve ser maior que zero"]


def preencher_vao(analise, k, q, L):
    campo_q, campo_L, _ = analise.vaos[k]
    campo_q.var.set(q)
    campo_L.var.set(L)


def test_viga_vao_sem_comprimento(raiz, erros):
    analise = JanelaViga(raiz).analise
    preencher_vao(analise, 0, "10", "0")
    analise.calcular()
    assert len(erros) == 1 and "positivo" in erros[0]


def test_viga_balanco_sem_carga(raiz, erros):
    analise = JanelaViga(raiz).analise
    preencher_vao(analise, 0, "10", "4")
    analise.bal_esq.escolha.combo.set("sim")
    analise.calcular()
    assert len(erros) == 1 and "q (kN/m)" in erros[0]


def test_viga_enviar_momento_sem_calcular(raiz, monkeypatch):
    avisos = []
    monkeypatch.setattr(janela_viga.messagebox, "showinfo", lambda *a, **k: avisos.append(a))
    JanelaViga(raiz).analise.enviar_momento()
    assert len(avisos) == 1


def test_viga_momento_da_analise_vai_para_o_dimensionamento(raiz, erros):
    janela = JanelaViga(raiz)
    analise = janela.analise
    analise.adicionar_vao()
    preencher_vao(analise, 0, "10", "4")
    preencher_vao(analise, 1, "10", "4")
    analise.bal_dir.escolha.combo.set("sim")
    analise.bal_dir.q.var.set("10")
    analise.bal_dir.L.var.set("1")
    analise.calcular()
    assert erros == []

    # o maior momento em módulo vem pré-selecionado: apoio central de 2 vãos iguais
    assert analise.combo_momento.get().startswith("Apoio 2")
    analise.enviar_momento()
    dim = janela.dimensionamento
    assert dim.mk.valor() == pytest.approx(abs(analise.resultado.momentos_apoio[1]), abs=1e-3)
    assert "Apoio 2" in dim.origem_mk.cget("text")
    assert janela.notebook.select() == str(dim)

    # editar Mk à mão apaga a indicação de origem
    dim.mk.var.set("50")
    assert dim.origem_mk.cget("text") == ""


def test_viga_secao_estreita_demais(raiz, erros):
    dim = JanelaViga(raiz).dimensionamento
    for nome, valor in dict(mk="5", fck="25", altura="50", base="6", c="2,5", fil="1",
                            fit="0,5", ca="50", bitola="16").items():
        getattr(dim, nome).var.set(valor)
    dim.calcular()
    assert len(erros) == 1 and "largura" in erros[0]
