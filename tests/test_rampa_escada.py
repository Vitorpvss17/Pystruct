import math

import pytest

from pystruct.calculo import escada, rampa


def dados_rampa(**alteracoes):
    base = dict(v=0.3, h=1.2, espessura=20, c=2.5, ca=50, fck=25, rev=1.0, bitola=10, bitola_sec=6.3)
    base.update(alteracoes)
    return rampa.DadosRampa(**base)


def test_rampa_angulo_e_altura_vertical():
    res = rampa.dimensionar(dados_rampa())
    alfa = math.atan(0.3 / 1.2)
    assert res.alfa == pytest.approx(math.degrees(alfa))
    # o cosseno deve ser calculado em radianos
    assert res.altura_vertical == pytest.approx(20 / math.cos(alfa))


def test_rampa_momento():
    res = rampa.dimensionar(dados_rampa())
    carga = (res.altura_vertical / 100 * 25 + 1.0) * 1.4
    assert res.carga == pytest.approx(carga)
    assert res.md == pytest.approx(carga * 1.2 ** 2 / 8 + 100 * 1.4 * 0.6 ** 2 / 1.2)


def test_rampa_horizontal_zero():
    with pytest.raises(ValueError):
        rampa.dimensionar(dados_rampa(h=0))


def test_rampa_usa_bitola_secundaria_informada():
    a = rampa.dimensionar(dados_rampa(bitola_sec=5))
    b = rampa.dimensionar(dados_rampa(bitola_sec=8))
    assert a.secundaria.n_barras > b.secundaria.n_barras


def dados_escada(**alteracoes):
    base = dict(h=3.0, espelho=17.5, piso=28, espessura=10, c=2.5, ca=50, fck=25,
                rev=1.0, com_acesso=True, bitola=10, bitola_sec=6.3)
    base.update(alteracoes)
    return escada.DadosEscada(**base)


def test_escada_geometria():
    res = escada.dimensionar(dados_escada())
    alfa = math.atan(17.5 / 28)
    assert res.alfa == pytest.approx(math.degrees(alfa))
    assert res.h1 == pytest.approx(10 / math.cos(alfa))
    assert res.hm == pytest.approx(res.h1 + 17.5 / 2)
    assert res.d == pytest.approx(res.hm - 2.5 - 0.5)


def test_escada_sobrecarga_de_acesso():
    com = escada.dimensionar(dados_escada(com_acesso=True))
    sem = escada.dimensionar(dados_escada(com_acesso=False))
    assert com.carga - sem.carga == pytest.approx(0.5 * 1.4)
    assert com.md == pytest.approx(com.carga * 9 / 8)
