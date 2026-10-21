"""Telas de rampa e escada: formulário e resultados em comum."""
from __future__ import annotations

import flet as ft

from ..calculo import escada, rampa
from ..calculo.laje_inclinada import SecaoLaje
from ..formatacao import formatar
from .componentes import CampoNumero, CartaoResultado, Entrada, Linha, ler_campos, secao

ESPESSURA = [Entrada("espessura", "Espessura da laje", "cm")]
MATERIAIS = [
    Entrada("c", "Cobrimento c", "cm"),
    Entrada("ca", "Aço CA", "kgf/mm²", "50"),
    Entrada("fck", "fck", "MPa"),
    Entrada("rev", "Revestimento", "kN/m²"),
]
ARMADURA = [
    Entrada("bitola", "Bitola principal", "mm"),
    Entrada("bitola_sec", "Bitola secundária", "mm"),
]


class TelaLajeInclinada:
    """Monta a tela a partir das entradas; as subclasses definem geometria e cálculo."""

    titulo = ""
    geometria: list[Entrada] = []

    def __init__(self):
        self.campos: dict[str, CampoNumero] = {}
        self.resultado = CartaoResultado()

        formulario = ft.Column(
            [
                secao("Geometria", self._criar_campos(self.geometria + ESPESSURA)),
                secao("Materiais e cargas", self._criar_campos(MATERIAIS) + self.controles_extras()),
                secao("Armadura", self._criar_campos(ARMADURA)),
                ft.FilledButton("Calcular", icon=ft.Icons.CALCULATE, on_click=self.calcular),
            ],
            spacing=20,
        )
        self.raiz = ft.Column(
            [
                ft.Text(self.titulo, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.ResponsiveRow(
                    [
                        ft.Container(formulario, col={"xs": 12, "md": 7}),
                        ft.Container(self.resultado, col={"xs": 12, "md": 5}),
                    ],
                    spacing=24,
                    run_spacing=24,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _criar_campos(self, entradas: list[Entrada]) -> list[ft.Control]:
        novos = {e.nome: CampoNumero(e) for e in entradas}
        self.campos.update(novos)
        return list(novos.values())

    # pontos de extensão

    def controles_extras(self) -> list[ft.Control]:
        """Controles de carga além do revestimento."""
        return []

    def valores_extras(self) -> dict:
        return {}

    def dimensionar(self, valores: dict) -> SecaoLaje:
        raise NotImplementedError

    def linhas_geometria(self, res: SecaoLaje) -> list[Linha]:
        return []

    def linha_area_aco(self, res: SecaoLaje) -> Linha:
        return Linha("Área de aço", res.flexao.as_calc, "cm²/m")

    # cálculo

    def calcular(self, _=None) -> None:
        valores = ler_campos(self.campos)
        if valores is None:
            self.resultado.mostrar_erro("Corrija os campos marcados.")
            return
        try:
            res = self.dimensionar({**valores, **self.valores_extras()})
        except (ValueError, ZeroDivisionError) as erro:
            self.resultado.mostrar_erro(str(erro))
            return

        fl = res.flexao
        self.resultado.mostrar([
            Linha("Inclinação α", res.alfa, "°", casas=2),
            *self.linhas_geometria(res),
            Linha("Md", res.md, "kN·m/m"),
            Linha("Altura útil d", res.d, "cm"),
            Linha("Linha neutra x", fl.x, "cm"),
            Linha("x/d", f"{formatar(fl.x_d)} - " + ("permitida" if fl.ductil else "não permitida"), alerta=not fl.ductil),
            self.linha_area_aco(res),
            Linha("Armadura principal", res.principal.descricao(), alerta=not res.principal.permitido),
            Linha("Armadura secundária", res.secundaria.descricao(), alerta=not res.secundaria.permitido),
        ])


class TelaRampa(TelaLajeInclinada):
    titulo = "Rampa"
    geometria = [
        Entrada("v", "V - distância vertical", "m"),
        Entrada("h", "H - distância horizontal", "m"),
    ]

    def dimensionar(self, valores: dict) -> rampa.ResultadoRampa:
        return rampa.dimensionar(rampa.DadosRampa(**valores))

    def linhas_geometria(self, res: rampa.ResultadoRampa) -> list[Linha]:
        return [Linha("Espessura na vertical", res.altura_vertical, "cm")]

    def linha_area_aco(self, res: rampa.ResultadoRampa) -> Linha:
        if res.armadura_permitida:
            return super().linha_area_aco(res)
        return Linha("Área de aço", "Não permitida (As < As,mín)", alerta=True)


class TelaEscada(TelaLajeInclinada):
    titulo = "Escada"
    geometria = [
        Entrada("h", "H - vão horizontal", "m"),
        Entrada("espelho", "e - espelho", "cm"),
        Entrada("piso", "s - piso", "cm"),
    ]

    def controles_extras(self) -> list[ft.Control]:
        self.acesso = ft.Switch(label="Escada com acesso", value=True, col=12)
        return [self.acesso]

    def valores_extras(self) -> dict:
        return {"com_acesso": bool(self.acesso.value)}

    def dimensionar(self, valores: dict) -> escada.ResultadoEscada:
        return escada.dimensionar(escada.DadosEscada(**valores))

    def linhas_geometria(self, res: escada.ResultadoEscada) -> list[Linha]:
        return [
            Linha("h1 - espessura na vertical", res.h1, "cm"),
            Linha("hm - espessura média", res.hm, "cm"),
        ]

    def linha_area_aco(self, res: escada.ResultadoEscada) -> Linha:
        return Linha("Área de aço", res.flexao.as_adotada, "cm²/m")
