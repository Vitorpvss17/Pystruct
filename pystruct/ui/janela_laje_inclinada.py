"""Base das janelas de rampa e escada: formulário e resultados em comum."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..calculo.laje_inclinada import SecaoLaje
from .componentes import Campo, JanelaEstrutura, Saida, formatar, mostrar_erro, titulo_secao


class JanelaLajeInclinada(JanelaEstrutura):
    """Monta as seções Geometria, Materiais e cargas, Armadura e Resultados.

    As subclasses acrescentam seus próprios campos e saídas em `criar_geometria`,
    `criar_cargas_extras` e `criar_saidas_geometria`, e fazem o cálculo em `dimensionar`.
    """

    def __init__(self, inicial: tk.Tk, titulo: str):
        super().__init__(inicial, titulo)
        f = self.conteudo
        self._linha = 0

        self.titulo("Geometria")
        self.criar_geometria()
        self.espessura = self.campo("Espessura da laje (cm):")

        self.titulo("Materiais e cargas")
        self.c = self.campo("c - cobrimento (cm):")
        self.ca = self.campo("CA (kgf/mm²):", "50")
        self.fck = self.campo("fck (MPa):")
        self.rev = self.campo("Revestimento (kN/m²):")
        self.criar_cargas_extras()

        self.titulo("Armadura")
        self.bitola = self.campo("Bitola principal (mm):")
        self.bitola_sec = self.campo("Bitola secundária (mm):")

        ttk.Button(f, text="Calcular", command=self.calcular).grid(
            row=self.proxima_linha(), column=1, sticky="w", padx=5, pady=10
        )

        self.titulo("Resultados")
        self.s_alfa = self.saida("Alfa (graus):")
        self.criar_saidas_geometria()
        self.s_md = self.saida("Md (kN·m/m):")
        self.s_x = self.saida("Linha neutra x (cm):")
        self.s_norma = self.saida("Verificação x/d:")
        self.s_as = self.saida("Área de aço (cm²/m):")
        self.s_principal = self.saida("Armadura principal:")
        self.s_secundaria = self.saida("Armadura secundária:")

    # montagem do formulário em linhas sequenciais

    def proxima_linha(self) -> int:
        self._linha += 1
        return self._linha - 1

    def titulo(self, texto: str) -> None:
        titulo_secao(self.conteudo, texto, self.proxima_linha())

    def campo(self, rotulo: str, padrao: str = "") -> Campo:
        return Campo(self.conteudo, self.proxima_linha(), rotulo, padrao)

    def saida(self, rotulo: str) -> Saida:
        return Saida(self.conteudo, self.proxima_linha(), rotulo)

    # pontos de extensão

    def criar_geometria(self) -> None:
        """Campos de geometria que vêm antes da espessura."""

    def criar_cargas_extras(self) -> None:
        """Campos de carga além do revestimento."""

    def criar_saidas_geometria(self) -> None:
        """Saídas que vêm logo depois do ângulo."""

    def dimensionar(self) -> SecaoLaje:
        raise NotImplementedError

    def mostrar_geometria(self, res: SecaoLaje) -> None:
        """Preenche as saídas criadas em `criar_saidas_geometria`."""

    def mostrar_area_aco(self, res: SecaoLaje) -> None:
        self.s_as.mostrar(res.flexao.as_calc)

    # cálculo

    def calcular(self) -> None:
        try:
            res = self.dimensionar()
        except (ValueError, ZeroDivisionError) as erro:
            mostrar_erro(self, erro)
            return

        self.s_alfa.mostrar(res.alfa, 2)
        self.mostrar_geometria(res)
        self.s_md.mostrar(res.md)
        self.s_x.mostrar(res.flexao.x)
        self.s_norma.mostrar(
            f"x/d = {formatar(res.flexao.x_d)} - " + ("permitida" if res.flexao.ductil else "não permitida")
        )
        self.mostrar_area_aco(res)
        self.s_principal.mostrar(res.principal.descricao())
        self.s_secundaria.mostrar(res.secundaria.descricao())
