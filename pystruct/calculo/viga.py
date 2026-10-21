"""Dimensionamento da seção transversal de viga à flexão."""
from __future__ import annotations

from dataclasses import dataclass

from . import armadura, flexao, materiais


@dataclass
class DadosSecaoViga:
    mk: float      # momento característico, em módulo (kN·m)
    fck: float     # MPa
    altura: float  # cm
    base: float    # cm
    c: float       # cobrimento (cm)
    fil: float     # diâmetro da armadura longitudinal (cm)
    fit: float     # diâmetro do estribo (cm)
    ca: float      # kgf/mm²
    bitola: float  # bitola escolhida para as barras (mm)


@dataclass
class ResultadoSecaoViga:
    md: float      # kN·m
    d: float       # cm
    flexao: flexao.ResultadoFlexao
    distribuicao: armadura.DistribuicaoViga


def dimensionar(dados: DadosSecaoViga) -> ResultadoSecaoViga:
    md = materiais.GAMA_F * abs(dados.mk)
    d = dados.altura - dados.c - dados.fit - dados.fil / 2
    res_flexao = flexao.dimensionar(md, dados.fck, dados.ca, d, dados.base)
    distribuicao = armadura.distribuir_barras_viga(
        res_flexao.as_calc, dados.bitola, dados.base, dados.c, dados.fit
    )
    return ResultadoSecaoViga(md=md, d=d, flexao=res_flexao, distribuicao=distribuicao)
