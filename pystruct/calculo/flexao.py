"""Dimensionamento à flexão simples de seção retangular."""
from __future__ import annotations

import math
from dataclasses import dataclass

from . import materiais

LIMITE_X_D = 0.45  # limite de ductilidade x/d


@dataclass
class ResultadoFlexao:
    fcd: float        # kN/cm²
    fyd: float        # kN/cm²
    x: float          # posição da linha neutra (cm)
    x_d: float        # relação x/d
    ductil: bool      # True se x/d < 0,45
    as_calc: float    # armadura calculada (cm²)
    as_min: float     # armadura mínima (cm²)

    @property
    def as_adotada(self) -> float:
        return max(self.as_calc, self.as_min)


def linha_neutra(md: float, fcd: float, d: float, bw: float) -> float:
    """Posição da linha neutra x (cm).

    md em kN·m, fcd em kN/cm², d e bw em cm.
    Resolve 0,272·fcd·bw·x² − 0,68·fcd·bw·d·x + Md = 0 e devolve a menor raiz.
    """
    a = 0.68 * 0.4 * fcd * bw
    b = -0.68 * fcd * d * bw
    c = md * 100
    if a == 0:
        raise ValueError("fck e a largura da seção devem ser maiores que zero")
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        raise ValueError("Linha neutra sem raízes reais: a seção não resiste ao momento")
    return (-b - math.sqrt(delta)) / (2 * a)


def area_aco(md: float, fyd: float, d: float, x: float) -> float:
    """Área de aço necessária (cm²). md em kN·m, fyd em kN/cm², d e x em cm."""
    return md * 100 / (fyd * (d - 0.4 * x))


def area_aco_minima(d: float) -> float:
    """Armadura mínima (cm²) usada no projeto: 0,15% de uma faixa de 100 cm."""
    return 0.15 * d


def dimensionar(md: float, fck: float, ca: float, d: float, bw: float) -> ResultadoFlexao:
    """Dimensiona a seção: md em kN·m, fck em MPa, ca em kgf/mm², d e bw em cm."""
    if d <= 0:
        raise ValueError("A altura útil d deve ser positiva; confira altura e cobrimento")
    fcd = materiais.fcd(fck)
    fyd = materiais.fyd(ca)
    x = linha_neutra(md, fcd, d, bw)
    return ResultadoFlexao(
        fcd=fcd,
        fyd=fyd,
        x=x,
        x_d=x / d,
        ductil=x / d < LIMITE_X_D,
        as_calc=area_aco(md, fyd, d, x),
        as_min=area_aco_minima(d),
    )
