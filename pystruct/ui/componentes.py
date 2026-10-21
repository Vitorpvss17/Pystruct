"""Componentes de interface reutilizados pelas janelas."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from ..formatacao import formatar, ler_numero

FONTE = ("Arial", 10)
FONTE_TITULO = ("Arial", 11, "bold")


def mostrar_erro(janela: tk.Misc, erro: Exception) -> None:
    messagebox.showerror("Não foi possível calcular", str(erro), parent=janela)


def titulo_secao(parent: tk.Misc, texto: str, row: int) -> None:
    ttk.Label(parent, text=texto, font=FONTE_TITULO).grid(
        row=row, column=0, columnspan=2, sticky="w", pady=(14, 4)
    )


class Campo:
    """Linha de formulário: rótulo + caixa de entrada numérica."""

    def __init__(self, parent: tk.Misc, row: int, rotulo: str, padrao: str = "", largura: int = 30, coluna: int = 0):
        self.rotulo = rotulo
        self.var = tk.StringVar(value=padrao)
        ttk.Label(parent, text=rotulo, font=FONTE).grid(row=row, column=coluna, sticky="w", padx=5, pady=2)
        self.entry = ttk.Entry(parent, textvariable=self.var, width=largura)
        self.entry.grid(row=row, column=coluna + 1, sticky="w", padx=5, pady=2)

    def valor(self) -> float:
        return ler_numero(self.var.get(), self.rotulo)

    def definir(self, valor: float) -> None:
        self.var.set(formatar(valor))


class Saida:
    """Linha de resultado: rótulo + caixa somente leitura."""

    def __init__(self, parent: tk.Misc, row: int, rotulo: str, largura: int = 40):
        self.var = tk.StringVar()
        ttk.Label(parent, text=rotulo, font=FONTE).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(parent, textvariable=self.var, width=largura, state="readonly").grid(
            row=row, column=1, sticky="w", padx=5, pady=2
        )

    def mostrar(self, valor: float | str, casas: int = 3) -> None:
        self.var.set(formatar(valor, casas) if isinstance(valor, (int, float)) else valor)

    def limpar(self) -> None:
        self.var.set("")


class Escolha:
    """Linha de formulário com uma lista de opções."""

    def __init__(self, parent: tk.Misc, row: int, rotulo: str, opcoes: list[str], padrao: int = 0):
        ttk.Label(parent, text=rotulo, font=FONTE).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.combo = ttk.Combobox(parent, values=opcoes, state="readonly", width=10)
        self.combo.current(padrao)
        self.combo.grid(row=row, column=1, sticky="w", padx=5, pady=2)

    def valor(self) -> str:
        return self.combo.get()


class AreaRolavel(ttk.Frame):
    """Frame com barra de rolagem vertical. Coloque os widgets em `self.conteudo`."""

    def __init__(self, parent: tk.Misc):
        super().__init__(parent)
        fundo = ttk.Style().lookup("TFrame", "background")
        self.canvas = tk.Canvas(self, highlightthickness=0, background=fundo)
        barra = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.conteudo = ttk.Frame(self.canvas, padding=10)
        self.canvas.create_window(0, 0, window=self.conteudo, anchor="nw")
        self.conteudo.bind(
            "<Configure>", lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Enter>", lambda _: self.canvas.bind_all("<MouseWheel>", self._rolar))
        self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all("<MouseWheel>"))

    def _rolar(self, evento: tk.Event) -> None:
        self.canvas.yview_scroll(int(-evento.delta / 120), "units")


class JanelaEstrutura(tk.Toplevel):
    """Base das janelas de dimensionamento: esconde a janela inicial e oferece 'Voltar'."""

    def __init__(self, inicial: tk.Tk, titulo: str, tamanho: str = "825x650"):
        super().__init__(inicial)
        self.inicial = inicial
        self.title(titulo)
        self.geometry(tamanho)

        ttk.Button(self, text="Voltar", command=self.voltar).pack(side="bottom", anchor="w", padx=10, pady=8)

        self.area = AreaRolavel(self)
        self.area.pack(fill="both", expand=True)
        self.conteudo = self.area.conteudo

        inicial.withdraw()
        self.protocol("WM_DELETE_WINDOW", inicial.destroy)

    def voltar(self) -> None:
        self.destroy()
        self.inicial.deiconify()
