"""Partes comuns de rampa e escada: laje inclinada armada em uma direção.

Cada estrutura calcula a própria carga e o próprio momento; daqui saem a
geometria da inclinação e o dimensionamento da faixa de 1 m de largura.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from . import armadura, flexao, materiais

# diâmetro estimado da barra para o cálculo de d, antes da bitola ser escolhida
DIAMETRO_ESTIMADO = 1.0  # cm
FAIXA = 100.0  # cm, dimensionamento por metro de largura


def inclinacao(subida: float, avanco: float) -> float:
    """Ângulo da laje com a horizontal, em radianos."""
    if avanco <= 0:
        raise ValueError("A projeção horizontal da inclinação deve ser maior que zero")
    return math.atan(subida / avanco)


def espessura_vertical(espessura: float, alfa: float) -> float:
    """Espessura da laje medida na vertical (mesma unidade de `espessura`)."""
    return espessura / math.cos(alfa)


def peso_proprio(espessura_cm: float) -> float:
    """Peso próprio de uma laje de concreto, em kN/m²."""
    return espessura_cm / 100 * materiais.PESO_ESPECIFICO_CONCRETO


def momento_biapoiado(carga: float, vao: float) -> float:
    """Momento máximo de laje biapoiada com carga uniforme (kN·m/m)."""
    return carga * vao ** 2 / 8


@dataclass(kw_only=True)
class SecaoLaje:
    d: float  # altura útil (cm)
    flexao: flexao.ResultadoFlexao
    principal: armadura.ArmaduraLaje
    secundaria: armadura.ArmaduraLaje


def dimensionar_secao(
    md: float, altura: float, c: float, fck: float, ca: float,
    espessura: float, bitola: float, bitola_sec: float,
) -> SecaoLaje:
    """Dimensiona a faixa de 1 m. `altura` é a altura usada no cálculo de d (cm)."""
    d = altura - c - DIAMETRO_ESTIMADO / 2
    res_flexao = flexao.dimensionar(md, fck, ca, d, FAIXA)
    return SecaoLaje(
        d=d,
        flexao=res_flexao,
        principal=armadura.armadura_principal_laje(res_flexao.as_calc, bitola, espessura),
        secundaria=armadura.armadura_secundaria_laje(res_flexao.as_calc, res_flexao.as_min, bitola_sec),
    )
