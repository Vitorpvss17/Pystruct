from __future__ import annotations

from tkinter import ttk

import ttkbootstrap

from .janela_escada import JanelaEscada
from .janela_rampa import JanelaRampa
from .janela_viga import JanelaViga

ESTRUTURAS = {
    "Rampa": JanelaRampa,
    "Escada": JanelaEscada,
    "Viga": JanelaViga,
}


class JanelaInicial(ttkbootstrap.Window):
    def __init__(self):
        super().__init__(title="Pystruct", themename="yeti")
        self.geometry("1025x650")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        ttk.Label(self, text="BEM VINDO AO PYSTRUCT!", font=("Arial", 30)).grid(row=1, column=0, pady=10)
        ttk.Label(self, text="Qual estrutura você gostaria de dimensionar?", font=("Arial", 10)).grid(
            row=2, column=0, pady=10
        )

        escolha = ttk.Frame(self)
        escolha.grid(row=3, column=0, pady=10)
        self.combo = ttk.Combobox(escolha, values=list(ESTRUTURAS), state="readonly")
        self.combo.current(0)
        self.combo.pack(side="left", padx=5)
        ttk.Button(escolha, text="Selecionar", command=self.abrir).pack(side="left", padx=5)

    def abrir(self) -> None:
        ESTRUTURAS[self.combo.get()](self)
