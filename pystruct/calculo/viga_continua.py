"""Análise de viga contínua pelo método dos deslocamentos.

Viga com N vãos, apoios simples, balanços opcionais nas extremidades,
carga uniformemente distribuída em cada trecho e seção constante.

As incógnitas são as rotações dos apoios internos. Os vãos extremos são
tratados como engastado-rotulados (rigidez 3EI/L) e os internos como
biengastados (4EI/L na extremidade e 2EI/L transmitido à outra).

O balanço é isostático: o momento que ele aplica no apoio extremo
(−q·a²/2) é conhecido. Ele entra no vão extremo como momento na extremidade
rotulada, e metade dele é transmitida à extremidade engastada.

Convenção dos momentos de engastamento: positivo na extremidade esquerda
e negativo na direita, de modo que o momento de extremidade direita de um
vão é diretamente o momento fletor no apoio (negativo quando traciona em cima).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Balanco:
    q: float  # carga (kN/m)
    L: float  # comprimento (m)

    @property
    def momento_apoio(self) -> float:
        """Momento fletor no apoio (negativo: traciona em cima)."""
        return -self.q * self.L ** 2 / 2

    def momento_em(self, distancia_ponta: float) -> float:
        """Momento fletor a uma distância da extremidade livre."""
        return -self.q * distancia_ponta ** 2 / 2


@dataclass
class ResultadoViga:
    q: list[float]                  # carga de cada vão (kN/m)
    L: list[float]                  # comprimento de cada vão (m)
    momentos_engastamento: list[tuple[float, float]]  # (esquerda, direita) por vão
    rigidez: np.ndarray             # matriz de rigidez K
    beta: np.ndarray                # soma dos momentos de engastamento em cada nó
    deslocabilidades: np.ndarray    # rotações D (K·D = −β)
    momentos_apoio: list[float]     # momento fletor em cada apoio, extremos = 0 (kN·m)
    reacoes: list[float]            # reação vertical em cada apoio (kN)
    cortantes: list[float]          # cortante no início de cada vão (kN)
    momentos_positivos: list[float]  # momento máximo em cada vão (kN·m)
    posicoes_maximo: list[float]    # posição do momento máximo a partir do início do vão (m)
    balanco_esq: Balanco | None = None
    balanco_dir: Balanco | None = None

    @property
    def n_vaos(self) -> int:
        return len(self.L)

    def momento_em(self, vao: int, x: float) -> float:
        """Momento fletor no vão `vao` a uma distância x (m) do seu apoio esquerdo."""
        return self.momentos_apoio[vao] + self.cortantes[vao] * x - self.q[vao] * x ** 2 / 2

    @property
    def posicoes_apoios(self) -> list[float]:
        """Abscissa de cada apoio, com x = 0 na ponta do balanço esquerdo (ou no 1º apoio)."""
        inicio = self.balanco_esq.L if self.balanco_esq else 0.0
        return [inicio + float(x) for x in np.concatenate([[0], np.cumsum(self.L)])]

    def diagrama(self, pontos_por_vao: int = 50) -> tuple[np.ndarray, np.ndarray]:
        """Coordenadas (x global, M) do diagrama de momentos fletores."""
        apoios = self.posicoes_apoios
        xs, ms = [], []
        if self.balanco_esq:
            x_local = np.linspace(0, self.balanco_esq.L, pontos_por_vao)
            xs.append(x_local)
            ms.append(np.array([self.balanco_esq.momento_em(x) for x in x_local]))
        for k, comp in enumerate(self.L):
            x_local = np.linspace(0, comp, pontos_por_vao)
            xs.append(apoios[k] + x_local)
            ms.append(np.array([self.momento_em(k, x) for x in x_local]))
        if self.balanco_dir:
            x_local = np.linspace(0, self.balanco_dir.L, pontos_por_vao)
            xs.append(apoios[-1] + x_local)
            ms.append(np.array([self.balanco_dir.momento_em(self.balanco_dir.L - x) for x in x_local]))
        return np.concatenate(xs), np.concatenate(ms)


def _momentos_engastamento(
    q: list[float], L: list[float], m_esq: float, m_dir: float
) -> list[tuple[float, float]]:
    """Momentos de engastamento (esq, dir) de cada vão.

    `m_esq` e `m_dir` são os momentos fletores conhecidos nos apoios extremos
    (zero sem balanço). Na convenção daqui, o momento de extremidade esquerda
    vale −M fletor e o de extremidade direita vale +M fletor.
    """
    n = len(L)
    fem = []
    for k in range(n):
        m = q[k] * L[k] ** 2 / 12
        esq, dir_ = m, -m
        if n == 1:
            esq, dir_ = -m_esq, m_dir
        elif k == 0:
            # libera a extremidade esquerda até o valor imposto pelo balanço
            dir_ += (-m_esq - esq) / 2
            esq = -m_esq
        elif k == n - 1:
            esq += (m_dir - dir_) / 2
            dir_ = m_dir
        fem.append((esq, dir_))
    return fem


def analisar(
    q: list[float], L: list[float], E: float, I: float,
    balanco_esq: Balanco | None = None, balanco_dir: Balanco | None = None,
) -> ResultadoViga:
    """Resolve a viga contínua. q em kN/m, L em m.

    Com seção constante o produto E·I se cancela e não altera os esforços,
    mas é mantido para que a matriz de rigidez tenha o significado físico.
    """
    n = len(L)
    if n == 0:
        raise ValueError("A viga precisa de pelo menos um vão")
    if len(q) != n:
        raise ValueError("Informe uma carga para cada vão")
    if any(comp <= 0 for comp in L):
        raise ValueError("Todos os vãos devem ter comprimento positivo")
    if E <= 0 or I <= 0:
        raise ValueError("E e I devem ser positivos")
    for balanco in (balanco_esq, balanco_dir):
        if balanco and balanco.L <= 0:
            raise ValueError("O comprimento do balanço deve ser positivo")

    m_extremo_esq = balanco_esq.momento_apoio if balanco_esq else 0.0
    m_extremo_dir = balanco_dir.momento_apoio if balanco_dir else 0.0

    EI = E * I
    fem = _momentos_engastamento(q, L, m_extremo_esq, m_extremo_dir)
    n_desl = n - 1

    # montagem da matriz de rigidez e do vetor β
    K = np.zeros((n_desl, n_desl))
    beta = np.zeros(n_desl)
    for k in range(n):
        esq, dir_ = k - 1, k  # índices das rotações nos apoios do vão k
        if n == 1:
            continue
        if k == 0:
            K[dir_, dir_] += 3 * EI / L[k]
            beta[dir_] += fem[k][1]
        elif k == n - 1:
            K[esq, esq] += 3 * EI / L[k]
            beta[esq] += fem[k][0]
        else:
            K[esq, esq] += 4 * EI / L[k]
            K[dir_, dir_] += 4 * EI / L[k]
            K[esq, dir_] += 2 * EI / L[k]
            K[dir_, esq] += 2 * EI / L[k]
            beta[esq] += fem[k][0]
            beta[dir_] += fem[k][1]

    D = np.linalg.solve(K, -beta) if n_desl else np.zeros(0)

    # momento em cada apoio interno = momento final na extremidade direita do vão à esquerda
    momentos_apoio = [m_extremo_esq]
    for k in range(n - 1):
        if k == 0:
            m_dir = fem[k][1] + 3 * EI / L[k] * D[k]
        else:
            m_dir = fem[k][1] + 2 * EI / L[k] * D[k - 1] + 4 * EI / L[k] * D[k]
        momentos_apoio.append(float(m_dir))
    momentos_apoio.append(m_extremo_dir)

    # cortantes, reações e momentos máximos de cada vão
    cortantes = [
        q[k] * L[k] / 2 + (momentos_apoio[k + 1] - momentos_apoio[k]) / L[k]
        for k in range(n)
    ]
    reacoes = [cortantes[0]]
    for k in range(1, n):
        reacoes.append(q[k - 1] * L[k - 1] - cortantes[k - 1] + cortantes[k])
    reacoes.append(q[-1] * L[-1] - cortantes[-1])
    if balanco_esq:
        reacoes[0] += balanco_esq.q * balanco_esq.L
    if balanco_dir:
        reacoes[-1] += balanco_dir.q * balanco_dir.L

    momentos_positivos, posicoes = [], []
    for k in range(n):
        x = cortantes[k] / q[k] if q[k] > 0 else 0.0
        x = min(max(x, 0.0), L[k])
        posicoes.append(x)
        momentos_positivos.append(momentos_apoio[k] + cortantes[k] * x - q[k] * x ** 2 / 2)

    return ResultadoViga(
        q=list(q),
        L=list(L),
        momentos_engastamento=fem,
        rigidez=K,
        beta=beta,
        deslocabilidades=D,
        momentos_apoio=momentos_apoio,
        reacoes=reacoes,
        cortantes=cortantes,
        momentos_positivos=momentos_positivos,
        posicoes_maximo=posicoes,
        balanco_esq=balanco_esq,
        balanco_dir=balanco_dir,
    )
