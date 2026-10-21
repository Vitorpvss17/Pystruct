"""Detalhamento de armaduras: número de barras, espaçamentos e camadas."""
from __future__ import annotations

import math
from dataclasses import dataclass

DIAMETRO_BRITA = 1.9  # cm (brita 1)

ESPACAMENTO_MAX_PRINCIPAL = 20.0  # cm
ESPACAMENTO_MAX_SECUNDARIA = 33.0  # cm
AREA_MIN_SECUNDARIA = 0.9  # cm²/m


def area_barra(bitola_mm: float) -> float:
    """Área da seção de uma barra (cm²)."""
    return math.pi * (bitola_mm / 10) ** 2 / 4


@dataclass
class ArmaduraLaje:
    n_barras: int        # barras por metro
    espacamento: float   # cm
    permitido: bool
    motivo: str = ""

    def descricao(self) -> str:
        if not self.permitido:
            return self.motivo
        return f"N01 D/: {self.n_barras}, c/ {self.espacamento:.1f} cm"


def armadura_principal_laje(as_: float, bitola_mm: float, espessura: float) -> ArmaduraLaje:
    """Armadura principal por metro de laje. as_ em cm²/m, espessura em cm."""
    n = math.ceil(as_ / area_barra(bitola_mm))
    s = 100 / n
    if s > ESPACAMENTO_MAX_PRINCIPAL:
        return ArmaduraLaje(n, s, False, f"Espaçamento não permitido (> {ESPACAMENTO_MAX_PRINCIPAL:.0f} cm)")
    if s > 2 * espessura:
        return ArmaduraLaje(n, s, False, "Espaçamento não permitido (> 2h)")
    return ArmaduraLaje(n, s, True)


def armadura_secundaria_laje(as_principal: float, as_min: float, bitola_mm: float) -> ArmaduraLaje:
    """Armadura de distribuição por metro de laje."""
    as_dis = max(0.2 * as_principal, 0.5 * as_min, AREA_MIN_SECUNDARIA)
    n = math.ceil(as_dis / area_barra(bitola_mm))
    s = 100 / n
    if s > ESPACAMENTO_MAX_SECUNDARIA:
        return ArmaduraLaje(n, s, False, "Barra não permitida")
    return ArmaduraLaje(n, s, True)


@dataclass
class DistribuicaoViga:
    n_barras: int
    ah: float                 # espaçamento horizontal livre (cm)
    av: float                 # espaçamento vertical livre (cm)
    barras_por_camada: int
    n_camadas: int
    barras_ultima_camada: int  # 0 quando a última camada está completa

    def barras_em_cada_camada(self) -> list[int]:
        """Quantidade de barras em cada camada, de baixo para cima."""
        camadas = [self.barras_por_camada] * self.n_camadas
        if self.barras_ultima_camada:
            camadas[-1] = self.barras_ultima_camada
        return camadas


def distribuir_barras_viga(as_: float, bitola_mm: float, bw: float, c: float, fit: float) -> DistribuicaoViga:
    """Distribui as barras longitudinais em camadas. Medidas em cm, bitola em mm."""
    phi = bitola_mm / 10
    n = math.ceil(as_ / area_barra(bitola_mm))
    ah = max(2.0, phi, 1.2 * DIAMETRO_BRITA)
    av = max(2.0, phi, 0.5 * DIAMETRO_BRITA)
    por_camada = int((bw + ah - 2 * c - 2 * fit) / (ah + phi))
    if por_camada < 1:
        raise ValueError("Nenhuma barra cabe na largura da viga com esses cobrimentos")
    return DistribuicaoViga(
        n_barras=n,
        ah=ah,
        av=av,
        barras_por_camada=por_camada,
        n_camadas=math.ceil(n / por_camada),
        barras_ultima_camada=n % por_camada,
    )
