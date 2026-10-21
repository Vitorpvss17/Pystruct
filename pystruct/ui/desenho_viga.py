"""Desenhos da viga com matplotlib: esquema estático e diagrama de momentos."""
from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes

from ..calculo.viga_continua import ResultadoViga

LARGURA_VAO = 8.0       # largura esquemática de cada vão (fora de escala)
LARGURA_BALANCO = 4.0
ALTURA_CARGA = 3.0
SETAS_POR_VAO = 3


def _apoio(ax: Axes, x: float) -> None:
    ax.plot([x - 1, x, x + 1, x - 1], [0, 1, 0, 0], color="black", lw=1)


def _carga(ax: Axes, x0: float, x1: float, cor: str) -> None:
    topo = 1 + ALTURA_CARGA
    ax.plot([x0, x0, x1, x1], [1, topo, topo, 1], color=cor, lw=1)
    for x in np.linspace(x0, x1, SETAS_POR_VAO + 2)[1:-1]:
        ax.plot([x, x], [topo, 1], color=cor, lw=1)
        ax.plot([x - 0.4, x, x + 0.4], [1.4, 1, 1.4], color=cor, lw=1)


def desenhar_esquema(ax: Axes, n_vaos: int, balanco_esq: bool, balanco_dir: bool) -> None:
    """Esquema da viga: apoios, vãos e carga distribuída (fora de escala)."""
    ax.clear()
    ax.axis("off")
    if n_vaos == 0:
        return

    x = 0.0
    trechos = []
    if balanco_esq:
        trechos.append((x, x + LARGURA_BALANCO, "tab:orange"))
        x += LARGURA_BALANCO
    apoios = [x]
    for _ in range(n_vaos):
        trechos.append((x, x + LARGURA_VAO, "tab:blue"))
        x += LARGURA_VAO
        apoios.append(x)
    if balanco_dir:
        trechos.append((x, x + LARGURA_BALANCO, "tab:orange"))
        x += LARGURA_BALANCO

    ax.plot([0, x], [1, 1], color="black", lw=2)
    for x0, x1, cor in trechos:
        _carga(ax, x0, x1, cor)
    for xa in apoios:
        _apoio(ax, xa)
    for k in range(n_vaos):
        meio = apoios[k] + LARGURA_VAO / 2
        ax.text(meio, 1 + ALTURA_CARGA + 0.4, f"vão {k + 1}", ha="center", fontsize=8)
    ax.set_ylim(-0.5, 1 + ALTURA_CARGA + 1.5)


def desenhar_diagrama_momentos(ax: Axes, res: ResultadoViga) -> None:
    """Diagrama de momentos fletores, com momentos positivos para baixo."""
    ax.clear()
    xs, ms = res.diagrama()
    ax.plot(xs, ms, color="tab:red", lw=1.5)
    ax.fill_between(xs, ms, 0, color="tab:red", alpha=0.15)
    ax.axhline(0, color="black", lw=1)
    ax.invert_yaxis()

    apoios_x = res.posicoes_apoios
    for x, m in zip(apoios_x, res.momentos_apoio):
        if m == 0:
            continue
        ax.annotate(f"{m:.2f}", (x, m), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    for k, (m, xm) in enumerate(zip(res.momentos_positivos, res.posicoes_maximo)):
        ax.annotate(f"{m:.2f}", (apoios_x[k] + xm, m), textcoords="offset points", xytext=(0, -12),
                    ha="center", fontsize=8)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("M (kN·m)")
    ax.set_xticks([xs[0], *apoios_x, xs[-1]])
    ax.grid(alpha=0.3)
