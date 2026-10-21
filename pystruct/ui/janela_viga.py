from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ..calculo import viga, viga_continua
from ..export import autocad, memoria
from . import desenho_viga
from .componentes import Campo, Escolha, JanelaEstrutura, Saida, formatar, mostrar_erro, titulo_secao


class CamposBalanco:
    """Escolha sim/não do balanço com os campos de carga e comprimento ao lado."""

    def __init__(self, parent: tk.Misc, row: int, rotulo: str, ao_mudar: Callable[[], None]):
        self.escolha = Escolha(parent, row, rotulo, ["sim", "não"], padrao=1)
        campos = ttk.Frame(parent)
        campos.grid(row=row, column=2, sticky="w")
        self.q = Campo(campos, 0, "q (kN/m)", largura=8)
        self.L = Campo(campos, 0, "L (m)", largura=8, coluna=2)
        self.escolha.combo.bind("<<ComboboxSelected>>", lambda _: (self._habilitar(), ao_mudar()))
        self._habilitar()

    @property
    def ativo(self) -> bool:
        return self.escolha.valor() == "sim"

    def _habilitar(self) -> None:
        estado = ["!disabled"] if self.ativo else ["disabled"]
        self.q.entry.state(estado)
        self.L.entry.state(estado)

    def balanco(self) -> viga_continua.Balanco | None:
        if not self.ativo:
            return None
        return viga_continua.Balanco(self.q.valor(), self.L.valor())


class PaginaAnalise(ttk.Frame):
    """Análise da viga contínua: vãos, cargas, esforços e diagrama."""

    def __init__(self, parent: tk.Misc, ao_escolher_momento: Callable[[str, float], None]):
        super().__init__(parent, padding=10)
        self.vaos: list[tuple[Campo, Campo, ttk.Frame]] = []
        self.resultado: viga_continua.ResultadoViga | None = None
        self.ao_escolher_momento = ao_escolher_momento
        self.momentos: dict[str, float] = {}

        titulo_secao(self, "Balanços", 0)
        self.bal_esq = CamposBalanco(self, 1, "Esquerdo:", self.atualizar_esquema)
        self.bal_dir = CamposBalanco(self, 2, "Direito:", self.atualizar_esquema)

        titulo_secao(self, "Vãos", 3)
        botoes = ttk.Frame(self)
        botoes.grid(row=4, column=0, columnspan=2, sticky="w")
        ttk.Button(botoes, text="+ vão", command=self.adicionar_vao).pack(side="left", padx=5)
        ttk.Button(botoes, text="− vão", command=self.remover_vao).pack(side="left", padx=5)
        self.frame_vaos = ttk.Frame(self)
        self.frame_vaos.grid(row=5, column=0, columnspan=2, sticky="w")

        self.fig_esquema = Figure(figsize=(6, 1.6), dpi=100, facecolor="white")
        self.ax_esquema = self.fig_esquema.add_subplot(111)
        self.canvas_esquema = FigureCanvasTkAgg(self.fig_esquema, master=self)
        self.canvas_esquema.get_tk_widget().grid(row=6, column=0, columnspan=2, pady=10)

        titulo_secao(self, "Seção", 7)
        self.E = Campo(self, 8, "Módulo de elasticidade E:", "30e6")
        self.I = Campo(self, 9, "Momento de inércia I:", "26785")

        acoes = ttk.Frame(self)
        acoes.grid(row=10, column=0, columnspan=2, sticky="w", pady=10)
        ttk.Button(acoes, text="Calcular", command=self.calcular).pack(side="left", padx=5)
        ttk.Button(acoes, text="Salvar memória de cálculo...", command=self.salvar_memoria).pack(side="left", padx=5)

        titulo_secao(self, "Resultados", 11)
        colunas = ("apoio", "m_apoio", "reacao", "vao", "m_pos")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=6)
        for col, texto in zip(colunas, ("Apoio", "M apoio (kN·m)", "Reação (kN)", "Vão", "M+ máx (kN·m)")):
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=110, anchor="center")
        self.tabela.grid(row=12, column=0, columnspan=3, sticky="w")

        self.fig_momentos = Figure(figsize=(6, 2.6), dpi=100, facecolor="white")
        self.ax_momentos = self.fig_momentos.add_subplot(111)
        self.canvas_momentos = FigureCanvasTkAgg(self.fig_momentos, master=self)
        self.canvas_momentos.get_tk_widget().grid(row=13, column=0, columnspan=3, pady=10)

        escolha = ttk.Frame(self)
        escolha.grid(row=14, column=0, columnspan=3, sticky="w")
        ttk.Label(escolha, text="Momento para dimensionar:").pack(side="left", padx=5)
        self.combo_momento = ttk.Combobox(escolha, state="readonly", width=35)
        self.combo_momento.pack(side="left", padx=5)
        ttk.Button(escolha, text="Dimensionar este momento", command=self.enviar_momento).pack(side="left", padx=5)

        self.adicionar_vao()

    # vãos

    def adicionar_vao(self) -> None:
        linha = ttk.Frame(self.frame_vaos)
        linha.pack(anchor="w")
        n = len(self.vaos) + 1
        q = Campo(linha, 0, f"Vão {n}:   q (kN/m)", largura=8)
        L = Campo(linha, 0, "L (m)", largura=8, coluna=2)
        self.vaos.append((q, L, linha))
        self.atualizar_esquema()

    def remover_vao(self) -> None:
        if len(self.vaos) > 1:
            *_, linha = self.vaos.pop()
            linha.destroy()
            self.atualizar_esquema()

    def atualizar_esquema(self) -> None:
        desenho_viga.desenhar_esquema(
            self.ax_esquema,
            len(self.vaos),
            self.bal_esq.ativo,
            self.bal_dir.ativo,
        )
        self.canvas_esquema.draw()

    # cálculo

    def calcular(self) -> None:
        try:
            q = [campo_q.valor() for campo_q, _, _ in self.vaos]
            L = [campo_L.valor() for _, campo_L, _ in self.vaos]
            res = viga_continua.analisar(
                q, L, self.E.valor(), self.I.valor(),
                balanco_esq=self.bal_esq.balanco(), balanco_dir=self.bal_dir.balanco(),
            )
        except (ValueError, ArithmeticError) as erro:
            mostrar_erro(self, erro)
            return

        self.resultado = res
        self.tabela.delete(*self.tabela.get_children())
        for k in range(res.n_vaos + 1):
            tem_vao = k < res.n_vaos
            self.tabela.insert("", "end", values=(
                k + 1,
                formatar(res.momentos_apoio[k]),
                formatar(res.reacoes[k]),
                k + 1 if tem_vao else "",
                formatar(res.momentos_positivos[k]) if tem_vao else "",
            ))

        desenho_viga.desenhar_diagrama_momentos(self.ax_momentos, res)
        self.fig_momentos.tight_layout()
        self.canvas_momentos.draw()

        self.momentos = {}
        for k, m in enumerate(res.momentos_apoio):
            if m != 0:
                self.momentos[f"Apoio {k + 1} (negativo): {formatar(m)}"] = m
        for k, m in enumerate(res.momentos_positivos):
            self.momentos[f"Vão {k + 1} (positivo): {formatar(m)}"] = m
        self.combo_momento.configure(values=list(self.momentos))
        self.combo_momento.set(max(self.momentos, key=lambda chave: abs(self.momentos[chave])))

    def enviar_momento(self) -> None:
        escolhido = self.combo_momento.get()
        if escolhido not in self.momentos:
            messagebox.showinfo("Dimensionamento", "Calcule a viga primeiro.", parent=self)
            return
        self.ao_escolher_momento(escolhido, self.momentos[escolhido])

    def salvar_memoria(self) -> None:
        if self.resultado is None:
            messagebox.showinfo("Memória de cálculo", "Calcule a viga primeiro.", parent=self)
            return
        caminho = filedialog.asksaveasfilename(
            parent=self, defaultextension=".txt", initialfile="memoria_viga.txt",
            filetypes=[("Texto", "*.txt")],
        )
        if caminho:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(memoria.memoria_viga_continua(self.resultado))


class PaginaDimensionamento(ttk.Frame):
    """Dimensionamento da seção à flexão e detalhamento das barras."""

    def __init__(self, parent: tk.Misc):
        super().__init__(parent, padding=10)
        self.ultimo: tuple[viga.DadosSecaoViga, viga.ResultadoSecaoViga] | None = None

        titulo_secao(self, "Dados", 0)
        self.mk = Campo(self, 1, "Mk - em módulo (kN·m):")
        self.origem_mk = ttk.Label(self, text="", foreground="gray")
        self.origem_mk.grid(row=1, column=2, sticky="w", padx=5)
        self.mk.var.trace_add("write", lambda *_: self.origem_mk.configure(text=""))
        self.fck = Campo(self, 2, "fck (MPa):")
        self.altura = Campo(self, 3, "Altura (cm):")
        self.base = Campo(self, 4, "Base (cm):")
        self.c = Campo(self, 5, "c - cobrimento (cm):")
        self.fil = Campo(self, 6, "φl - diâmetro longitudinal (cm):")
        self.fit = Campo(self, 7, "φt - diâmetro do estribo (cm):")
        self.ca = Campo(self, 8, "CA (kgf/mm²):", "50")
        self.bitola = Campo(self, 9, "Bitola das barras (mm):")

        acoes = ttk.Frame(self)
        acoes.grid(row=10, column=0, columnspan=2, sticky="w", pady=10)
        ttk.Button(acoes, text="Calcular", command=self.calcular).pack(side="left", padx=5)
        ttk.Button(acoes, text="Gerar script do AutoCAD...", command=self.gerar_autocad).pack(side="left", padx=5)

        titulo_secao(self, "Resultados", 11)
        self.s_md = Saida(self, 12, "Md (kN·m):")
        self.s_d = Saida(self, 13, "d (cm):")
        self.s_x = Saida(self, 14, "Linha neutra x (cm):")
        self.s_norma = Saida(self, 15, "Verificação x/d:")
        self.s_as = Saida(self, 16, "Área de aço calculada (cm²):")
        self.s_as_min = Saida(self, 17, "Área de aço mínima (cm²):")
        self.s_n = Saida(self, 18, "Número de barras:")
        self.s_ah = Saida(self, 19, "ah (cm):")
        self.s_av = Saida(self, 20, "av (cm):")
        self.s_por_camada = Saida(self, 21, "Barras em cada camada:")
        self.s_camadas = Saida(self, 22, "Nº de camadas:")
        self.s_ultima = Saida(self, 23, "Barras na última camada:")

    def usar_momento(self, origem: str, momento: float) -> None:
        """Preenche Mk com um momento vindo da análise da viga."""
        self.mk.definir(abs(momento))
        self.origem_mk.configure(text=f"da análise: {origem.split(':')[0]}")

    def calcular(self) -> None:
        try:
            dados = viga.DadosSecaoViga(
                mk=self.mk.valor(),
                fck=self.fck.valor(),
                altura=self.altura.valor(),
                base=self.base.valor(),
                c=self.c.valor(),
                fil=self.fil.valor(),
                fit=self.fit.valor(),
                ca=self.ca.valor(),
                bitola=self.bitola.valor(),
            )
            res = viga.dimensionar(dados)
        except (ValueError, ZeroDivisionError) as erro:
            mostrar_erro(self, erro)
            return

        self.ultimo = (dados, res)
        dist = res.distribuicao
        self.s_md.mostrar(res.md)
        self.s_d.mostrar(res.d)
        self.s_x.mostrar(res.flexao.x)
        self.s_norma.mostrar(
            f"x/d = {res.flexao.x_d:.3f} - " + ("permitida" if res.flexao.ductil else "não permitida")
        )
        self.s_as.mostrar(res.flexao.as_calc)
        self.s_as_min.mostrar(res.flexao.as_min)
        self.s_n.mostrar(f"N01 D/: {dist.n_barras}")
        self.s_ah.mostrar(dist.ah, 2)
        self.s_av.mostrar(dist.av, 2)
        self.s_por_camada.mostrar(str(dist.barras_por_camada))
        self.s_camadas.mostrar(str(dist.n_camadas))
        self.s_ultima.mostrar(str(dist.barras_ultima_camada))

    def gerar_autocad(self) -> None:
        if self.ultimo is None:
            messagebox.showinfo("AutoCAD", "Calcule a seção primeiro.", parent=self)
            return
        caminho = filedialog.asksaveasfilename(
            parent=self, defaultextension=".scr", initialfile="Viga.scr",
            filetypes=[("Script do AutoCAD", "*.scr")],
        )
        if not caminho:
            return
        dados, res = self.ultimo
        script = autocad.script_secao_viga(dados.base, dados.altura, dados.c, dados.fit, dados.bitola, res.distribuicao)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(script)


class JanelaViga(JanelaEstrutura):
    def __init__(self, inicial: tk.Tk):
        super().__init__(inicial, "Viga", "1025x650")
        self.notebook = ttk.Notebook(self.conteudo)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.analise = PaginaAnalise(self.notebook, self.dimensionar_momento)
        self.dimensionamento = PaginaDimensionamento(self.notebook)
        self.notebook.add(self.analise, text="Análise")
        self.notebook.add(self.dimensionamento, text="Dimensionamento")

    def dimensionar_momento(self, origem: str, momento: float) -> None:
        self.dimensionamento.usar_momento(origem, momento)
        self.notebook.select(self.dimensionamento)
