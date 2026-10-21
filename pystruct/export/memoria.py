"""Memória de cálculo em texto da análise da viga contínua."""
from __future__ import annotations

import numpy as np

from ..calculo.viga_continua import Balanco, ResultadoViga


def _balanco(balanco: Balanco | None) -> str:
    if balanco is None:
        return "não"
    return f"q = {balanco.q} kN/m, L = {balanco.L} m, M no apoio = {balanco.momento_apoio:.4f} kN·m"


def memoria_viga_continua(res: ResultadoViga) -> str:
    with np.printoptions(precision=4, suppress=False):
        linhas = [
            "MEMÓRIA DE CÁLCULO - VIGA CONTÍNUA",
            "",
            f"Vãos (m): {res.L}",
            f"Cargas (kN/m): {res.q}",
            f"Balanço esquerdo: {_balanco(res.balanco_esq)}",
            f"Balanço direito: {_balanco(res.balanco_dir)}",
            "",
            f"Momentos de engastamento (esq, dir) por vão: {res.momentos_engastamento}",
            f"Vetor beta: {res.beta}",
            f"Matriz de rigidez K:\n{res.rigidez}",
            f"Deslocabilidades D: {res.deslocabilidades}",
            "",
            f"Momentos nos apoios (kN·m): {res.momentos_apoio}",
            f"Reações (kN): {res.reacoes}",
            f"Momentos positivos máximos (kN·m): {res.momentos_positivos}",
            f"Posição dos máximos a partir do início de cada vão (m): {res.posicoes_maximo}",
        ]
    return "\n".join(linhas) + "\n"
