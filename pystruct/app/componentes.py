"""Componentes do app Flet reutilizados pelas telas."""
from __future__ import annotations

from dataclasses import dataclass

import flet as ft

from ..formatacao import formatar, ler_numero

# largura de cada campo na grade de 12 colunas: 1 por linha no celular, 2 no tablet, 3 no desktop
COLUNAS_CAMPO = {"xs": 12, "sm": 6, "lg": 4}


@dataclass(frozen=True)
class Entrada:
    """Descrição de um campo numérico; `nome` é o nome do campo na dataclass `Dados...`."""
    nome: str
    rotulo: str
    unidade: str = ""
    padrao: str = ""


class CampoNumero(ft.TextField):
    def __init__(self, entrada: Entrada):
        super().__init__(
            label=entrada.rotulo,
            suffix=entrada.unidade or None,
            value=entrada.padrao,
            keyboard_type=ft.KeyboardType.NUMBER,
            col=COLUNAS_CAMPO,
            on_change=self._limpar_erro,
        )
        self.rotulo = entrada.rotulo

    def _limpar_erro(self, _=None) -> None:
        self.error = None

    def valor(self) -> float:
        """Lê o número digitado; se for inválido, marca o campo e relança o erro."""
        try:
            return ler_numero(self.value or "", self.rotulo)
        except ValueError:
            self.error = "Digite um número"
            raise


def ler_campos(campos: dict[str, CampoNumero]) -> dict[str, float] | None:
    """Lê todos os campos, marcando cada um inválido. None se algum falhar."""
    valores, ok = {}, True
    for nome, campo in campos.items():
        try:
            valores[nome] = campo.valor()
        except ValueError:
            ok = False
    return valores if ok else None


def secao(titulo: str, controles: list[ft.Control]) -> ft.Control:
    return ft.Column(
        [ft.Text(titulo, theme_style=ft.TextThemeStyle.TITLE_MEDIUM), ft.ResponsiveRow(controles)],
        spacing=8,
    )


@dataclass
class Linha:
    rotulo: str
    valor: float | str
    unidade: str = ""
    casas: int = 3
    alerta: bool = False

    def texto(self) -> str:
        valor = formatar(self.valor, self.casas) if isinstance(self.valor, (int, float)) else self.valor
        return f"{valor} {self.unidade}".strip()


class CartaoResultado(ft.Card):
    """Cartão com a lista de resultados, ou a mensagem de erro do cálculo."""

    def __init__(self):
        self.lista = ft.Column(spacing=6)
        super().__init__(
            content=ft.Container(
                ft.Column([ft.Text("Resultados", theme_style=ft.TextThemeStyle.TITLE_MEDIUM), self.lista]),
                padding=16,
            ),
        )
        self.limpar()

    def limpar(self) -> None:
        self.lista.controls = [ft.Text("Preencha os dados e clique em Calcular.", color=ft.Colors.ON_SURFACE_VARIANT)]
        self.linhas: list[Linha] = []
        self.erro: str | None = None

    def mostrar(self, linhas: list[Linha]) -> None:
        self.linhas, self.erro = linhas, None
        self.lista.controls = [self._linha(linha) for linha in linhas]

    def mostrar_erro(self, mensagem: str) -> None:
        self.linhas, self.erro = [], mensagem
        self.lista.controls = [
            ft.Row(
                [ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.ERROR),
                 ft.Text(mensagem, color=ft.Colors.ERROR, expand=True)],
            )
        ]

    @staticmethod
    def _linha(linha: Linha) -> ft.Control:
        cor = ft.Colors.ERROR if linha.alerta else None
        return ft.Row(
            [
                ft.Text(linha.rotulo, expand=True),
                ft.Text(linha.texto(), weight=ft.FontWeight.BOLD, color=cor, selectable=True),
            ],
        )
