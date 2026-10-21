"""App Flet: navegação entre as estruturas."""
from __future__ import annotations

import flet as ft

from .tela_laje_inclinada import TelaEscada, TelaRampa


class TelaEmMigracao:
    titulo = "Viga"

    def __init__(self):
        self.raiz = ft.Column(
            [
                ft.Text(self.titulo, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Text("A viga ainda está sendo migrada. Use por enquanto a versão desktop: python -m pystruct"),
            ]
        )


TELAS = [
    (TelaRampa, ft.Icons.ACCESSIBLE),
    (TelaEscada, ft.Icons.STAIRS),
    (TelaEmMigracao, ft.Icons.HORIZONTAL_RULE),
]


def main(page: ft.Page) -> None:
    page.title = "Pystruct"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.SYSTEM

    # as telas são criadas uma vez, para não perder o que foi digitado ao trocar de aba
    telas = [classe() for classe, _ in TELAS]
    conteudo = ft.Container(telas[0].raiz, expand=True, padding=16)

    def selecionar(e: ft.Event) -> None:
        conteudo.content = telas[e.control.selected_index].raiz

    if page.platform in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS):
        page.navigation_bar = ft.NavigationBar(
            destinations=[ft.NavigationBarDestination(icon=icone, label=t.titulo) for t, (_, icone) in zip(telas, TELAS)],
            on_change=selecionar,
        )
        page.add(ft.SafeArea(conteudo, expand=True))
    else:
        menu = ft.NavigationRail(
            destinations=[ft.NavigationRailDestination(icon=icone, label=t.titulo) for t, (_, icone) in zip(telas, TELAS)],
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            on_change=selecionar,
        )
        page.add(ft.Row([menu, ft.VerticalDivider(width=1), conteudo], expand=True))
