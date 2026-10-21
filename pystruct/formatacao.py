"""Formatação de números para exibição, com vírgula decimal."""


def formatar(valor: float, casas: int = 3) -> str:
    return f"{valor:.{casas}f}".replace(".", ",")


def ler_numero(texto: str, rotulo: str) -> float:
    """Converte o texto digitado em número, aceitando vírgula decimal."""
    try:
        return float(texto.strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"O campo \"{rotulo}\" deve ser um número.") from None
