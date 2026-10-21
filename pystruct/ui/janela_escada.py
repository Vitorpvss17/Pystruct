from __future__ import annotations

import tkinter as tk

from ..calculo import escada
from .componentes import Escolha
from .janela_laje_inclinada import JanelaLajeInclinada


class JanelaEscada(JanelaLajeInclinada):
    def __init__(self, inicial: tk.Tk):
        super().__init__(inicial, "Escada")

    def criar_geometria(self) -> None:
        self.h = self.campo("H - vão horizontal (m):")
        self.espelho = self.campo("e - espelho (cm):")
        self.piso = self.campo("s - piso (cm):")

    def criar_cargas_extras(self) -> None:
        self.acesso = Escolha(self.conteudo, self.proxima_linha(), "A escada possui acesso?", ["sim", "não"])

    def criar_saidas_geometria(self) -> None:
        self.s_h1 = self.saida("h1 - espessura na vertical (cm):")
        self.s_hm = self.saida("hm - espessura média (cm):")

    def dimensionar(self) -> escada.ResultadoEscada:
        return escada.dimensionar(escada.DadosEscada(
            h=self.h.valor(),
            espelho=self.espelho.valor(),
            piso=self.piso.valor(),
            espessura=self.espessura.valor(),
            c=self.c.valor(),
            ca=self.ca.valor(),
            fck=self.fck.valor(),
            rev=self.rev.valor(),
            com_acesso=self.acesso.valor() == "sim",
            bitola=self.bitola.valor(),
            bitola_sec=self.bitola_sec.valor(),
        ))

    def mostrar_geometria(self, res: escada.ResultadoEscada) -> None:
        self.s_h1.mostrar(res.h1)
        self.s_hm.mostrar(res.hm)

    def mostrar_area_aco(self, res: escada.ResultadoEscada) -> None:
        self.s_as.mostrar(res.flexao.as_adotada)
