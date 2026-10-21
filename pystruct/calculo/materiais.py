"""Constantes e resistências de cálculo dos materiais."""

GAMA_C = 1.4   # coeficiente de minoração do concreto
GAMA_S = 1.15  # coeficiente de minoração do aço
GAMA_F = 1.4   # coeficiente de majoração das ações

PESO_ESPECIFICO_CONCRETO = 25.0  # kN/m³


def fcd(fck_mpa: float) -> float:
    """Resistência de cálculo do concreto, em kN/cm² (fck entra em MPa)."""
    return (fck_mpa / GAMA_C) / 10


def fyd(ca: float) -> float:
    """Resistência de cálculo do aço, em kN/cm².

    `ca` é o número da categoria do aço (50 para CA-50), em kgf/mm²,
    que numericamente é usado como kN/cm².
    """
    return ca / GAMA_S
