"""Dimensionamento de rampa (laje inclinada armada em uma direção)."""
from __future__ import annotations

import math
from dataclasses import dataclass

from . import materiais
from .laje_inclinada import SecaoLaje, dimensionar_secao, espessura_vertical, inclinacao, momento_biapoiado, peso_proprio


@dataclass
class DadosRampa:
    v: float           # distância vertical (m)
    h: float           # distância horizontal (m)
    espessura: float   # espessura da laje (cm)
    c: float           # cobrimento (cm)
    ca: float          # categoria do aço (kgf/mm²)
    fck: float         # MPa
    rev: float         # carga de revestimento (kN/m²)
    bitola: float      # bitola principal (mm)
    bitola_sec: float  # bitola secundária (mm)


@dataclass(kw_only=True)
class ResultadoRampa(SecaoLaje):
    alfa: float             # inclinação (graus)
    altura_vertical: float  # espessura medida na vertical (cm)
    carga: float            # carga de cálculo (kN/m²)
    md: float               # momento de cálculo (kN·m/m)

    @property
    def armadura_permitida(self) -> bool:
        return self.flexao.as_calc >= self.flexao.as_min


def dimensionar(dados: DadosRampa) -> ResultadoRampa:
    if dados.h <= 0:
        raise ValueError("A distância horizontal deve ser maior que zero")

    alfa = inclinacao(dados.v, dados.h)
    altura_vertical = espessura_vertical(dados.espessura, alfa)

    carga = (peso_proprio(altura_vertical) + dados.rev) * materiais.GAMA_F
    md = momento_biapoiado(carga, dados.h) + (100 * materiais.GAMA_F * (dados.h / 2) ** 2) / dados.h

    secao = dimensionar_secao(
        md, altura_vertical, dados.c, dados.fck, dados.ca, dados.espessura, dados.bitola, dados.bitola_sec
    )
    return ResultadoRampa(
        **vars(secao),
        alfa=math.degrees(alfa),
        altura_vertical=altura_vertical,
        carga=carga,
        md=md,
    )
