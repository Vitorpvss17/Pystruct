"""Testes das telas Flet, sem abrir janela: o Flet só atualiza a tela ao fim dos eventos."""
import pytest

from pystruct.app.tela_laje_inclinada import TelaEscada, TelaRampa
from pystruct.calculo import escada, rampa

RAMPA = dict(v="0,3", h="1,2", espessura="20", c="2,5", ca="50", fck="25", rev="1", bitola="10", bitola_sec="6,3")
ESCADA = dict(h="3", espelho="17,5", piso="28", espessura="10", c="2,5", ca="50", fck="25",
              rev="1", bitola="10", bitola_sec="6,3")


def preencher(tela, valores):
    for nome, valor in valores.items():
        tela.campos[nome].value = valor


def linha(tela, rotulo):
    return next(l for l in tela.resultado.linhas if l.rotulo == rotulo)


def test_rampa_mostra_o_mesmo_md_do_back_end():
    tela = TelaRampa()
    preencher(tela, RAMPA)
    tela.calcular()
    assert tela.resultado.erro is None
    esperado = rampa.dimensionar(rampa.DadosRampa(v=0.3, h=1.2, espessura=20, c=2.5, ca=50, fck=25,
                                                  rev=1, bitola=10, bitola_sec=6.3))
    assert linha(tela, "Md").valor == pytest.approx(esperado.md)
    assert linha(tela, "Md").texto() == f"{esperado.md:.3f} kN·m/m".replace(".", ",")


def test_escada_usa_o_switch_de_acesso():
    tela = TelaEscada()
    preencher(tela, ESCADA)
    tela.calcular()
    com = linha(tela, "Md").valor
    tela.acesso.value = False
    tela.calcular()
    sem = linha(tela, "Md").valor
    dados = dict(h=3, espelho=17.5, piso=28, espessura=10, c=2.5, ca=50, fck=25, rev=1, bitola=10, bitola_sec=6.3)
    assert com == pytest.approx(escada.dimensionar(escada.DadosEscada(com_acesso=True, **dados)).md)
    assert sem == pytest.approx(escada.dimensionar(escada.DadosEscada(com_acesso=False, **dados)).md)


def test_campos_invalidos_ficam_marcados():
    tela = TelaRampa()
    preencher(tela, {**RAMPA, "fck": "abc", "c": ""})
    tela.calcular()
    assert tela.resultado.erro == "Corrija os campos marcados."
    assert tela.campos["fck"].error and tela.campos["c"].error
    assert tela.campos["v"].error is None

    # corrigir o campo apaga a marcação
    tela.campos["fck"]._limpar_erro()
    assert tela.campos["fck"].error is None


def test_erro_do_calculo_aparece_no_cartao():
    tela = TelaRampa()
    preencher(tela, {**RAMPA, "h": "0"})
    tela.calcular()
    assert tela.resultado.erro == "A distância horizontal deve ser maior que zero"
    assert tela.resultado.linhas == []


def test_aviso_quando_secao_nao_e_ductil():
    tela = TelaEscada()
    preencher(tela, {**ESCADA, "h": "7", "espessura": "6", "fck": "15"})  # x/d ≈ 0,52
    tela.calcular()
    assert tela.resultado.erro is None
    assert linha(tela, "x/d").alerta
