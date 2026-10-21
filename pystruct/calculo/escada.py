"""Dimensionamento de escada (laje inclinada com degraus, armada em uma direção)."""
from __future__ import annotations

import math
from dataclasses import dataclass

from . import materiais
from .laje_inclinada import SecaoLaje, dimensionar_secao, espessura_vertical, inclinacao, momento_biapoiado, peso_proprio

SOBRECARGA_COM_ACESSO = 3.0  # kN/m²
SOBRECARGA_SEM_ACESSO = 2.5  # kN/m²


@dataclass
class DadosEscada:
    h: float           # vão horizontal (m)
    espelho: float     # altura do degrau (cm)
    piso: float        # largura do degrau (cm)
    espessura: float   # espessura da laje (cm)
    c: float           # cobrimento (cm)
    ca: float          # kgf/mm²
    fck: float         # MPa
    rev: float         # kN/m²
    com_acesso: bool
    bitola: float      # mm
    bitola_sec: float  # mm


@dataclass(kw_only=True)
class ResultadoEscada(SecaoLaje):
    alfa: float   # graus
    h1: float     # espessura medida na vertical (cm)
    hm: float     # espessura média com os degraus (cm)
    carga: float  # kN/m²
    md: float     # kN·m/m


def dimensionar(dados: DadosEscada) -> ResultadoEscada:
    if dados.piso <= 0:
        raise ValueError("O piso do degrau deve ser maior que zero")

    alfa = inclinacao(dados.espelho, dados.piso)
    h1 = espessura_vertical(dados.espessura, alfa)
    hm = h1 + dados.espelho / 2

    sobrecarga = SOBRECARGA_COM_ACESSO if dados.com_acesso else SOBRECARGA_SEM_ACESSO
    carga = (peso_proprio(h1) + dados.rev + sobrecarga) * materiais.GAMA_F
    md = momento_biapoiado(carga, dados.h)

    secao = dimensionar_secao(md, hm, dados.c, dados.fck, dados.ca, dados.espessura, dados.bitola, dados.bitola_sec)
    return ResultadoEscada(
        **vars(secao),
        alfa=math.degrees(alfa),
        h1=h1,
        hm=hm,
        carga=carga,
        md=md,
    )
