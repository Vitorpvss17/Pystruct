import math

import pytest

from pystruct.calculo import armadura, flexao, materiais


def test_resistencias_de_calculo():
    assert materiais.fcd(25) == pytest.approx(25 / 1.4 / 10)
    assert materiais.fyd(50) == pytest.approx(50 / 1.15)


def test_linha_neutra_satisfaz_equilibrio():
    md, fcd, d, bw = 30.0, materiais.fcd(25), 45.0, 20.0
    x = flexao.linha_neutra(md, fcd, d, bw)
    # Md = 0,68·fcd·bw·x·(d − 0,4x)
    assert 0.68 * fcd * bw * x * (d - 0.4 * x) == pytest.approx(md * 100)
    assert 0 < x < d


def test_linha_neutra_sem_solucao():
    with pytest.raises(ValueError):
        flexao.linha_neutra(md=10_000, fcd=1.0, d=10, bw=10)


def test_dimensionar():
    res = flexao.dimensionar(md=30, fck=25, ca=50, d=45, bw=20)
    assert res.ductil == (res.x / 45 < 0.45)
    assert res.as_calc == pytest.approx(30 * 100 / (res.fyd * (45 - 0.4 * res.x)))
    assert res.as_min == pytest.approx(0.15 * 45)


def test_area_barra():
    assert armadura.area_barra(10) == pytest.approx(math.pi * 1 ** 2 / 4)


def test_armadura_principal_laje():
    arm = armadura.armadura_principal_laje(as_=4.0, bitola_mm=8, espessura=12)
    assert arm.n_barras == math.ceil(4.0 / armadura.area_barra(8))
    assert arm.espacamento == pytest.approx(100 / arm.n_barras)
    assert arm.permitido


def test_armadura_principal_laje_espacamento_excessivo():
    arm = armadura.armadura_principal_laje(as_=0.5, bitola_mm=10, espessura=12)
    assert not arm.permitido


def test_armadura_secundaria_usa_minimo_absoluto():
    arm = armadura.armadura_secundaria_laje(as_principal=1.0, as_min=0.5, bitola_mm=5)
    assert arm.n_barras == math.ceil(0.9 / armadura.area_barra(5))
