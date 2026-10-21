import pytest

from pystruct.calculo import armadura, viga
from pystruct.export import autocad

# Viga.scr gerado pela versão original: viga 20x60, c = 3, estribo 0,5 cm, barras de 10 mm.
# Na versão original algumas linhas saíam como "CIRCLE" (sem "_"); aqui todas usam "_CIRCLE".
SCRIPT_ORIGINAL = """_RECTANGLE 0,0 20.0,60.0 _RECTANGLE 3.0,3.0 17.0,57.0 _RECTANGLE 3.5,3.5 16.5,56.5
_CIRCLE 4.0,4.0 0.5 _CIRCLE 7.28,4.0 0.5 _CIRCLE 10.56,4.0 0.5 _CIRCLE 13.84,4.0 0.5
_CIRCLE 4.0,7.0 0.5 _CIRCLE 7.28,7.0 0.5 _CIRCLE 10.56,7.0 0.5 _CIRCLE 13.84,7.0 0.5
_CIRCLE 4.0,10.0 0.5 _CIRCLE 7.28,10.0 0.5"""


def _tokens(script):
    """Separa comandos e números para comparar com tolerância."""
    saida = []
    for tok in script.split():
        if tok.startswith("_"):
            saida.append(tok)
        else:
            saida.extend(float(v) for v in tok.split(","))
    return saida


def test_distribuicao_em_camadas():
    dist = armadura.distribuir_barras_viga(as_=7.5, bitola_mm=10, bw=20, c=3, fit=0.5)
    assert dist.n_barras == 10
    assert dist.ah == pytest.approx(2.28)
    assert dist.av == pytest.approx(2.0)
    assert dist.barras_por_camada == 4
    assert dist.barras_em_cada_camada() == [4, 4, 2]


def test_script_autocad_igual_ao_original():
    dist = armadura.distribuir_barras_viga(as_=7.5, bitola_mm=10, bw=20, c=3, fit=0.5)
    script = autocad.script_secao_viga(base=20, altura=60, c=3, fit=0.5, bitola_mm=10, distribuicao=dist)
    assert _tokens(script) == pytest.approx(_tokens(SCRIPT_ORIGINAL))


def test_viga_nao_cabe_nenhuma_barra():
    with pytest.raises(ValueError):
        armadura.distribuir_barras_viga(as_=5, bitola_mm=10, bw=5, c=3, fit=0.5)


def test_dimensionar_secao_viga():
    dados = viga.DadosSecaoViga(mk=50, fck=25, altura=50, base=20, c=3, fil=1.25, fit=0.5, ca=50, bitola=12.5)
    res = viga.dimensionar(dados)
    assert res.md == pytest.approx(70)
    assert res.d == pytest.approx(50 - 3 - 0.5 - 1.25 / 2)
    assert res.flexao.ductil
    assert res.distribuicao.n_barras * armadura.area_barra(12.5) >= res.flexao.as_calc
