"""Script (.scr) do AutoCAD com o desenho da seção transversal da viga."""
from __future__ import annotations

from ..calculo.armadura import DistribuicaoViga


def _retangulo(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"_RECTANGLE\n{x1},{y1}\n{x2},{y2}\n"


def _circulo(x: float, y: float, r: float) -> str:
    return f"_CIRCLE\n{x},{y}\n{r}\n"


def script_secao_viga(
    base: float,
    altura: float,
    c: float,
    fit: float,
    bitola_mm: float,
    distribuicao: DistribuicaoViga,
) -> str:
    """Desenha forma, cobrimento, estribo e barras longitudinais (medidas em cm)."""
    phi = bitola_mm / 10
    raio = phi / 2
    face_estribo = c + fit

    partes = [
        _retangulo(0, 0, base, altura),                                   # forma
        _retangulo(c, c, base - c, altura - c),                           # cobrimento
        _retangulo(face_estribo, face_estribo, base - face_estribo, altura - face_estribo),  # estribo
    ]

    y = face_estribo + raio
    for n_barras in distribuicao.barras_em_cada_camada():
        x = face_estribo + raio
        for _ in range(n_barras):
            partes.append(_circulo(x, y, raio))
            x += distribuicao.ah + phi
        y += distribuicao.av + phi

    return "".join(partes)
