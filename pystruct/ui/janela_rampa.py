from __future__ import annotations

import tkinter as tk

from ..calculo import rampa
from .janela_laje_inclinada import JanelaLajeInclinada


class JanelaRampa(JanelaLajeInclinada):
    def __init__(self, inicial: tk.Tk):
        super().__init__(inicial, "Rampa")

    def criar_geometria(self) -> None:
        self.v = self.campo("V - distância vertical (m):")
        self.h = self.campo("H - distância horizontal (m):")

    def criar_saidas_geometria(self) -> None:
        self.s_altura = self.saida("Espessura na vertical (cm):")

    def dimensionar(self) -> rampa.ResultadoRampa:
        return rampa.dimensionar(rampa.DadosRampa(
            v=self.v.valor(),
            h=self.h.valor(),
            espessura=self.espessura.valor(),
            c=self.c.valor(),
            ca=self.ca.valor(),
            fck=self.fck.valor(),
            rev=self.rev.valor(),
            bitola=self.bitola.valor(),
            bitola_sec=self.bitola_sec.valor(),
        ))

    def mostrar_geometria(self, res: rampa.ResultadoRampa) -> None:
        self.s_altura.mostrar(res.altura_vertical)

    def mostrar_area_aco(self, res: rampa.ResultadoRampa) -> None:
        if res.armadura_permitida:
            self.s_as.mostrar(res.flexao.as_calc)
        else:
            self.s_as.mostrar("Não permitida (As < As,mín)")
