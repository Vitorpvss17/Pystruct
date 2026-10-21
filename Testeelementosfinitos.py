import numpy as np
import sympy as sp
import math as mt
import tkinter as tk
from tkinter import *
from tkinter import ttk, Text
from ttkbootstrap import Style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def abrir_janela():
    opcao = comboboxinicio.get()
    if opcao == "Rampa":
        print('rampa')
    elif opcao == "Escada":
        print('escada')
    else:
        VigaNewWindow(opcao)
def fechar_janela():
    root.destroy()

# Janela principal
root = tk.Tk()
style = Style(theme = 'pulse')
root = style.master
root.geometry("825x650")
root.title('Dimestruct')
#root.geometry("Expansive")
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(2, weight=1)
#root.grid_rowconfigure(0, weight=1)
#root.grid_rowconfigure(2, weight=1)

# opções do combobox
val = ['Rampa', 'Escada', 'Viga']

#Criação do Combobox
comboboxinicio = ttk.Combobox(root, values=val)
comboboxinicio.grid(row=1, column=1)
# Texto de seleção
T1 = ttk.Label(
    text='Qual estrutura voce gostaria de dimensionar?',
    font=('Arial', 30)


)
T1.grid(row=0, column=1)
# botão de seleção
B1 = ttk.Button(
    root,
    text='Selecionar',
    command=abrir_janela
)

B1.grid(row=2, column=1)




#janela da estrutura Viga
def VigaNewWindow(opcao):
    VigaNewindow = tk.Toplevel()
    VigaNewindow.title(opcao)
    VigaNewindow.geometry("825x650")
    

    # criando barra de rolagem
    barra = Scrollbar(VigaNewindow)
    canvas = Canvas(VigaNewindow, yscrollcommand = barra.set)
    barra.config(command=canvas.yview)
    barra.pack(side='right', fill='y')


    frame = Frame(canvas)
    canvas.pack(side='top', fill='both', expand=True)
    canvas.create_window(0,0, window=frame)


    #criando as paginas
    notebook = ttk.Notebook(frame)
    notebook.grid()
    #Pagína de Analise
    page1 = ttk.Frame(notebook)
    notebook.add(page1, text='Analise')

    #apagando o texto ao clicar
    def clear_text(event):
        event.widget.delete('1.0', tk.END)
   
   # Armazenando balanços
    labelbal = ttk.Label(page1,
                        text='Balanços:',
                        font=('Arial', 10)
                        )
    labelbal.grid(row=2, column=0)
    # armazenando valor do balanço a direita
    labelbaldir = ttk.Label(page1,
                        text='Dir:',
                        font=('Arial', 10)
                        )
    labelbaldir.place(x=150, y=5)

    
    optionsp = ['sim', 'não']
    passeiocombod = ttk.Combobox(page1, values = optionsp)
    passeiocombod.place(x=180, y=1)
    passeiocombod.current(1)      

    # armazenando valor do balanço a esquerda
    labelbalesq = ttk.Label(page1,
                        text='Esq:',
                        font=('Arial', 10)
                        )
    labelbalesq.place(x=350, y=5)
    
  
    optionsp = ['sim', 'não']
    passeiocomboe = ttk.Combobox(page1, values = optionsp)
    passeiocomboe.place(x=385, y=1) 
    passeiocomboe.current(1)

    # Armazenando Nº de elementos e criando desenho da viga
    labelel = ttk.Label(page1,
                        text='Nº elementos:',
                        font=('Arial', 10)
                        )
    labelel.grid(row=4, column=0)
    forca_elem1 = []
    largura_elem1 = []
    forca_elem = []
    largura_elem = [] 
    counter = tk.IntVar(value=0)
    labelF = ttk.Label(page1,
                        text='F(KN):',
                        font=('Arial', 10)
                        )
    labelL = ttk.Label(page1,
                            text='L(m):',
                            font=('Arial', 10)
                            )
    def increment():
        counter.set(counter.get() + 1)
        Fvt = Text(page1, width=5, height=1, bd=1, relief='sunken')
        Fvt.place(x=(200 + (counter.get()-1)*60), y=90)
        forca_elem1.append(Fvt)  # adiciona o valor de Fvt convertido em float à lista forca_elem
        Lvt = Text(page1, width=5, height=1, bd=1, relief='sunken')
        Lvt.place(x=(200 + (counter.get()-1)*60), y=320)
        largura_elem1.append(Lvt)  # adiciona o valor de Lvt convertido em float à lista largura_elem
        labelF.place(x=150, y=95)
        labelL.place(x=150, y=325)



    def decrement():
        if counter.get() > 0:
            counter.set(counter.get() - 1)
            if len(forca_elem1) > 0: 
                Fvt = forca_elem1.pop()
                Fvt.destroy()
                

            if len(largura_elem1) > 0: 
                Lvt = largura_elem1.pop()
                Lvt.destroy()
            
            if counter.get() == 0:
                labelF.destroy()
                labelL.destroy()

    global max_x
    max_x = 0
    
    
    def Desenho_viga():
        global passeiovalord, passeiovalore, max_x
        passeiovalord = passeiocombod.get()
        passeiovalore = passeiocomboe.get()
        if passeiovalore == 'sim' and passeiovalord == 'sim':
            # cria figura do Matplotlib
            fig = Figure(figsize=(3, 2), dpi=100, facecolor='white')
            # cria objeto FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=page1)
            # exibe o objeto na tela
            canvas.get_tk_widget().grid(row=8, column=1, pady=40)
            # cria eixo para o gráfico
            ax = fig.add_subplot(111)
            # plota o primeiro desenho
            ax.plot([1, 2, 3, 1, 2, 10, 9, 11, 10, 2, 2, 10, 10, 8, 7.5, 8, 8.5, 8, 8, 6, 6, 6.5, 6, 5.5, 6, 4, 4.5, 4, 3.5, 4, 4], 
                    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3, 1, 1, 1.3, 1, 1.3, 1, 5])
            ax.axis('off')
            max_x = max(ax.lines[0].get_xdata())
            x_shift = max_x + 2 
            x2 = [x_shift-3, 1, 1, 1, -3, -3, -2, -2.5, -2, -1.5, -2, -2, 0, 0, -0.5, 0, 0.5]
            x2[1:] = [x + x_shift for x in x2[1:]]
            y2 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
            ax.plot(x2, y2)
            x3 = [2, -2, -2, -2, 2, 2, 1, 1.5, 1, 0.5, 1, 1, -1, -1, -0.5, -1, -1.5]
            y3 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
            ax.plot(x3, y3)
            # atualiza a tela
            canvas.draw()
            

        elif passeiovalord == 'sim' and passeiovalore == 'não':
          # cria figura do Matplotlib
            fig = Figure(figsize=(3, 2), dpi=100, facecolor='white')
            # cria objeto FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=page1)
            # exibe o objeto na tela
            canvas.get_tk_widget().grid(row=8, column=1, pady=40)
            # cria eixo para o gráfico
            ax = fig.add_subplot(111)
            # plota o primeiro desenho
            ax.plot([1, 2, 3, 1, 2, 10, 9, 11, 10, 2, 2, 10, 10, 8, 7.5, 8, 8.5, 8, 8, 6, 6, 6.5, 6, 5.5, 6, 4, 4.5, 4, 3.5, 4, 4], 
                    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3, 1, 1, 1.3, 1, 1.3, 1, 5])
            ax.axis('off')
            # obtem o valor máximo de x do primeiro desenho
            max_x = max(ax.lines[0].get_xdata())
            x_shift = max_x + 2 
            x2 = [x_shift-3, 1, 1, 1, -3, -3, -2, -2.5, -2, -1.5, -2, -2, 0, 0, -0.5, 0, 0.5]
            x2[1:] = [x + x_shift for x in x2[1:]]
            y2 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
            ax.plot(x2, y2)
            # atualiza a tela
            canvas.draw()
        
        elif passeiovalord == 'não' and passeiovalore == 'sim':
            # cria figura do Matplotlib
            fig = Figure(figsize=(3, 2), dpi=100, facecolor='white')
            # cria objeto FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=page1)
            # exibe o objeto na tela
            canvas.get_tk_widget().grid(row=8, column=1, pady=40)
            # cria eixo para o gráfico
            ax = fig.add_subplot(111)
            # plota o primeiro desenho
            ax.plot([1, 2, 3, 1, 2, 10, 9, 11, 10, 2, 2, 10, 10, 8, 7.5, 8, 8.5, 8, 8, 6, 6, 6.5, 6, 5.5, 6, 4, 4.5, 4, 3.5, 4, 4], 
                    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3, 1, 1, 1.3, 1, 1.3, 1, 5])
            ax.axis('off')
            x2 = [2, -2, -2, -2, 2, 2, 1, 1.5, 1, 0.5, 1, 1, -1, -1, -0.5, -1, -1.5]
            y2 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
            ax.plot(x2, y2)
            # atualiza a tela
            canvas.draw()


        else:
            # cria figura do Matplotlib
            fig = Figure(figsize=(3, 2), dpi=100, facecolor='white')
            # cria objeto FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=page1)
            # exibe o objeto na tela
            canvas.get_tk_widget().grid(row=8, column=1, pady=40)
            # cria eixo para o gráfico
            ax = fig.add_subplot(111)
            # plota o primeiro desenho
            ax.plot([1, 2, 3, 1, 2, 10, 9, 11, 10, 2, 2, 10, 10, 8, 7.5, 8, 8.5, 8, 8, 6, 6, 6.5, 6, 5.5, 6, 4, 4.5, 4, 3.5, 4, 4], 
                    [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3, 1, 1, 1.3, 1, 1.3, 1, 5])
            ax.axis('off')
            # atualiza a tela
            canvas.draw()



    def verificar_valor(*args):

        if counter.get() > 0:
            if counter.get() == 1:
                Desenho_viga()
            else:
                # cria eixo para o gráfico
                fig = Figure(figsize=(3, 2), dpi=100, facecolor='white')
                canvas = FigureCanvasTkAgg(fig, master=page1)
                canvas.draw()
                canvas.get_tk_widget().grid(row=8, column=1, pady=50)
                ax = fig.add_subplot(111)
                

                # plota o primeiro desenho
                ax.plot([1, 2, 3, 1, 2, 10, 9, 11, 10, 2, 2, 10, 10, 8, 7.5, 8, 8.5, 8, 8, 6, 6, 6.5, 6, 5.5, 6, 4, 4.5, 4, 3.5, 4, 4], 
                        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3, 1, 1, 1.3, 1, 1.3, 1, 5])
                ax.axis('off')

                # obtem o valor máximo de x do primeiro desenho
                max_x = max(ax.lines[0].get_xdata())   
                

                # plota os desenhos subsequentes
                for i in range(1, counter.get()):
                    # adiciona o valor máximo a todos os valores de x do próximo desenho
                    x_shift = max_x + 2 
                    x2 = [x_shift-3, -2, 2, 1, 2, 3, 1, 2, 2, -3, -3, -1, -1.5, -1, -0.5, -1, -1]
                    x2[1:] = [x + x_shift for x in x2[1:]]
                    y2 = [1, 1, 1, 0, 1, 0, 0, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5]
                    ax.plot(x2, y2)
                    ax.axis('off')
                    max_x = max(ax.lines[-1].get_xdata()) # atualiza o valor máximo de x para o próximo desenho
                    if passeiovalore == 'sim' and passeiovalord == 'sim':
                        x_shift = max_x + 2 
                        x2 = [x_shift-3, 1, 1, 1, -3, -3, -2, -2.5, -2, -1.5, -2, -2, 0, 0, -0.5, 0, 0.5]
                        x2[1:] = [x + x_shift for x in x2[1:]]
                        y2 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
                        ax.plot(x2, y2)
                        x3 = [2, -2, -2, -2, 2, 2, 1, 1.5, 1, 0.5, 1, 1, -1, -1, -0.5, -1, -1.5]
                        y3 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
                        ax.plot(x3, y3)
                    elif passeiovalord == 'não' and passeiovalore == 'sim':
                        x2 = [2, -2, -2, -2, 2, 2, 1, 1.5, 1, 0.5, 1, 1, -1, -1, -0.5, -1, -1.5]
                        y2 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
                        ax.plot(x2, y2)
                    elif passeiovalord == 'sim' and passeiovalore == 'não':
                        x_shift = max_x + 2 
                        x2 = [x_shift-3, 1, 1, 1, -3, -3, -2, -2.5, -2, -1.5, -2, -2, 0, 0, -0.5, 0, 0.5]
                        x2[1:] = [x + x_shift for x in x2[1:]]
                        y2 = [1, 1, 1, 5, 5, 1, 1, 1.3, 1, 1.3, 1, 5, 5, 1, 1.3, 1, 1.3]
                        ax.plot(x2, y2)

                    
                canvas.draw()
        else:
            # Remove o desenho da tela, se houver
            for widget in page1.grid_slaves():
                if int(widget.grid_info()['row']) == 8 and int(widget.grid_info()['column']) == 1:
                    widget.grid_forget()
                   
    # definir altura da linha vazia
    page1.grid_rowconfigure(2, minsize=20)

    # adicionar frame vazio na linha vazia
    empty_frame = tk.Frame(page1, width=10, height=20)
    empty_frame.grid(row=3, column=0)

    entry = ttk.Entry(page1, textvariable=counter)
    entry.configure(state='readonly')
    entry.grid(row=4, column=1)

    increment_button = ttk.Button(page1, text="+1", command=increment)
    increment_button.place(x=490, y=40)

    decrement_button = ttk.Button(page1, text="-1", command=decrement)
    decrement_button.place(x=450, y=40)
    counter.trace('w', verificar_valor) # Adiciona o trace na variável
    
    


    
    def Evalor():
        global evalor
        evalor = et.get('1.0', 'end')
        evalor = float(evalor)

    labele = ttk.Label(page1,
                        text='Modulo de elásticidade (cm):',
                        font=('Arial', 10)
                        )
    et = Text(page1, width=50, height=1, bd=3, relief='sunken')
    et.insert("1.0", "30e6") # valor padrão de módulo de elasticidade para o concreto
    labele.grid(row=10, column=0, pady= 10, padx= 10)
    et.bind('<Button-1>', clear_text)
    et.grid(row=10, column=1, pady= 10, padx= 10)
    botaoe = ttk.Button(
        page1,
        text='ok!',
        command=Evalor
    )
    botaoe.grid(row=10, column=2, pady= 10, padx= 10)

    def Ivalor():
        global ivalor
        ivalor = it.get('1.0', 'end')
        ivalor = float(ivalor)

    labeli = ttk.Label(page1,
                        text='Momento de Inércia (cm):',
                        font=('Arial', 10)
                        )
    it = Text(page1, width=50, height=1, bd=3, relief='sunken')
    it.insert("1.0", "26785") # valor padrão de momento de inércia para uma viga retangular de 30x60cm
    labeli.grid(row=11, column=0)
    it.bind('<Button-1>', clear_text)
    it.grid(row=11, column=1)
    botaoi = ttk.Button(
        page1,
        text='ok!',
        command=Ivalor
    )
    botaoi.grid(row=11, column=2)

    def theta_valor():
        global thetavalor
        thetavalor = thetat.get('1.0', 'end')
        thetavalor = float(thetavalor)

    labeltheta = ttk.Label(page1,
                        text='Angulo theta (°):',
                        font=('Arial', 10)
                        )
    thetat = Text(page1, width=50, height=1, bd=3, relief='sunken')
    thetat.insert("1.0", "26785") # valor padrão de momento de inércia para uma viga retangular de 30x60cm
    labeltheta.grid(row=12, column=0)
    thetat.bind('<Button-1>', clear_text)
    thetat.grid(row=12, column=1)
    botaotheta = ttk.Button(
        page1,
        text='ok!',
        command=Ivalor
    )
    botaotheta.grid(row=12, column=2)


    def area_valor():
        global thetavalor
        thetavalor = thetat.get('1.0', 'end')
        thetavalor = float(thetavalor)

    labeltheta = ttk.Label(page1,
                        text='Angulo theta (°):',
                        font=('Arial', 10)
                        )
    thetat = Text(page1, width=50, height=1, bd=3, relief='sunken')
    thetat.insert("1.0", "26785") # valor padrão de momento de inércia para uma viga retangular de 30x60cm
    labeltheta.grid(row=12, column=0)
    thetat.bind('<Button-1>', clear_text)
    thetat.grid(row=12, column=1)
    botaotheta = ttk.Button(
        page1,
        text='ok!',
        command=Ivalor
    )
    botaotheta.grid(row=12, column=2)

   
    def metodo_dos_elementos_finitos():

        
    botaomef = ttk.Button(page1, text='calcular', command=metodo_dos_elementos_finitos)
    botaomef.grid(row=14, column=0, pady= 10)
    
    def mostrar_valores():



    botaomv = ttk.Button(page1, text='Mostrar valores', command=mostrar_valores)
    botaomv.grid(row=15, column=0, pady= 10)

    



    #Pagina de Dimensionamento
    page2 = ttk.Frame(notebook)
    notebook.add(page2, text='Dimensionamento')
    # armazenando momento mk:
    def Mkvalor():
        global mkvalor
        mkvalor = mkt.get('1.0', 'end')
        mkvalor = float(mkvalor)
    labelmk = ttk.Label(page2,
                         text='Mk (KN/m):',
                         font=('Arial', 10)
                         )
    mkt = Text(page2, width=50, height=1, bd=3, relief='sunken')
    mkt.insert("1.0", "Digite o valor do Momento Mk(em módulo)")
    labelmk.grid(row=2, column=0)
    mkt.bind('<Button-1>', clear_text)
    mkt.grid(row=2, column=1)
    botaomk = ttk.Button(
        page2,
        text='ok!',
        command=Mkvalor
    )
    botaomk.grid(row=2, column=2)

    # armazenando valor de Fck
    labelFck = tk.Label(page2,
                        text='Fck (Mpa):',
                        font=('Arial', 10)
                        )
    Fck = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    Fck.insert("1.0", "Digite o valor do Fck")
    labelFck.grid(row=3, column=0)
    Fck.bind('<Button-1>', clear_text)
    Fck.grid(row=3, column=1)

    def valorFck():
        global Fckvalor
        Fckvalor = Fck.get('1.0', 'end')
        Fckvalor = float(Fckvalor)

    botaoFck = ttk.Button(
        page2,
        text='ok!',
        command=valorFck
    )
    botaoFck.grid(row=3, column=2)

    # armazenando valor da altura

    labelaltura = tk.Label(page2,
                           text='Altura (cm):',
                           font=('Arial', 10)
                           )
    altura = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    altura.insert("1.0", "Digite o valor do Hy da viga")
    labelaltura.grid(row=4, column=0)
    altura.bind('<Button-1>', clear_text)
    altura.grid(row=4, column=1)

    def valoraltura():
        global alturavalor
        alturavalor = altura.get('1.0', 'end')
        alturavalor = float(alturavalor)

    botaoaltura = ttk.Button(
        page2,
        text='ok!',
        command=valoraltura
    )
    botaoaltura.grid(row=4, column=2)

    # armazenando distância horizontal
    labelh = tk.Label(page2,
                      text='Base (cm):',
                      font=('Arial', 10)
                      )
    h = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    h.insert("1.0", "Digite o valor do Hx da viga")
    labelh.grid(row=5, column=0)
    h.bind('<Button-1>', clear_text)
    h.grid(row=5, column=1)

    def valorh():
        global hvalor
        hvalor = h.get('1.0', 'end')
        hvalor = float(hvalor)

    botaoh = ttk.Button(
        page2,
        text='ok!',
        command=valorh
    )
    botaoh.grid(row=5, column=2)

    # armazenando dimensôes do cobrimento
    labelc = tk.Label(page2,
                      text='c (cm):',
                      font=('Arial', 10)
                      )
    c = Text(page2, width=50, height=1, bd=3, relief='sunken')
    c.insert("1.0", "Digite o valor do cobrimento")
    labelc.grid(row=6, column=0)
    c.bind('<Button-1>', clear_text)
    c.grid(row=6, column=1)

    def valorc():
        global cvalor
        cvalor = c.get('1.0', 'end')
        cvalor = float(cvalor)

    botaoc = ttk.Button(
        page2,
        text='ok!',
        command=valorc
    )
    botaoc.grid(row=6, column=2)

    # armazenando valor de fil
    labelfil = tk.Label(page2,
                      text='fil (cm):',
                      font=('Arial', 10)
                      )
    filt = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    filt.insert("1.0", "Digite o valor do diâmetro longitudinal")
    labelfil.grid(row=7, column=0)
    filt.bind('<Button-1>', clear_text)
    filt.grid(row=7, column=1)

    def valorfil():
        global filvalor
        filvalor = filt.get('1.0', 'end')
        filvalor = float(filvalor)

    botaofil = ttk.Button(
        page2,
        text='ok!',
        command=valorfil
    )
    botaofil.grid(row=7, column=2)

    # armazenando valor de fit
    labelfit = tk.Label(page2,
                        text='fit (cm):',
                        font=('Arial', 10)
                        )
    fitt = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    fitt.insert("1.0", "Digite o valor do diâmetro transversal")
    labelfit.grid(row=8, column=0)
    fitt.bind('<Button-1>', clear_text)
    fitt.grid(row=8, column=1)

    def valorfit():
        global fitvalor
        fitvalor = fitt.get('1.0', 'end')
        fitvalor = float(fitvalor)

    botaofit = ttk.Button(
        page2,
        text='ok!',
        command=valorfit
    )
    botaofit.grid(row=8, column=2)

    # armazenando a resistência do aço
    labelca = tk.Label(page2,
                       text='CA (kgf/mm2):',
                       font=('Arial', 10)
                       )
    ca = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    ca.insert("1.0", "Digite o valor da resistência do aço")
    labelca.grid(row=9, column=0)
    ca.bind('<Button-1>', clear_text)
    ca.grid(row=9, column=1)

    def valorca():
        global cavalor
        cavalor = ca.get('1.0', 'end')
        cavalor = float(cavalor)

    botaoca = ttk.Button(
        page2,
        text='ok!',
        command=valorca
    )
    botaoca.grid(row=9, column=2)

    # calculando momento

    def valormomento():
        global valormd
        valormd = 1.4 * mkvalor
        Md.configure(state='normal')
        Md.delete('1.0', 'end')
        Md.insert('1.0', valormd)

        Md.configure(state='disabled')

    labelMd = tk.Label(page2,
                       text='Momento (KN/m2):',
                       font=('Arial', 10)
                       )
    Md = Text(page2,  width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelMd.grid(row=10, column=0)
    Md.grid(row=10, column=1)

    botaoMd = ttk.Button(
        page2,
        text='calcular Momento',
        command=valormomento

    )
    botaoMd.grid(row=10, column=2)

    # Calculando a linha neutra

    def valorlinhaneutra():
        global d
        global Fcd
        global Fyd
        Fyd = cavalor / 1.15
        fil = 1
        Fcd = (Fckvalor / 1.4) / 10
        d = alturavalor - cvalor - fitvalor - (fil / 2)
        a = 0.68 * 0.4 * Fcd * hvalor
        b = - 0.68 * Fcd * d * hvalor
        C = valormd * 100
        delta = (b ** 2) - 4 * a * C
        if a == 0:
            ln.configure(state='normal')
            ln.delete('1.0', 'end')
            ln.insert('1.0', 'O valor de a, deve ser diferente de 0')

            ln.configure(state='disabled')

        elif delta < 0:
            ln.configure(state='normal')
            ln.delete('1.0', 'end')
            ln.insert('1.0', 'Sem raízes reais')

            ln.configure(state='disabled')


        else:
            global lnvalor
            x1 = (-b + delta ** (1 / 2)) / (2 * a)
            x2 = (-b - delta ** (1 / 2)) / (2 * a)
            if x1 > x2:
                lnvalor = x2
            elif x1 < x2:
                lnvalor = x1

            ln.configure(state='normal')
            ln.delete('1.0', 'end')
            ln.insert('1.0', lnvalor)

            ln.configure(state='disabled')

    labelln = tk.Label(page2,
                       text='Linha neutra (ln):',
                       font=('Arial', 10)
                       )
    ln = Text(page2, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelln.grid(row=11, column=0)
    ln.grid(row=11, column=1)

    botaoln = ttk.Button(
        page2,
        text='calcular linha neutra',
        command=valorlinhaneutra

    )
    botaoln.grid(row=11, column=2)

    def vernorma():
        vernorma = lnvalor / d
        if vernorma >= 0.45:
            vernormat.configure(state='normal')
            vernormat.delete('1.0', 'end')
            vernormat.insert('1.0', 'Viga não permitida')

            vernormat.configure(state='disabled')
        else:
            vernormat.configure(state='normal')
            vernormat.delete('1.0', 'end')
            vernormat.insert('1.0', 'Viga permitida')

            vernormat.configure(state='disabled')

    labelvern = tk.Label(page2,
                         text='Verificação da norma:',
                         font=('Arial', 10)
                         )
    vernormat = Text(page2,  width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelvern.grid(row=12, column=0)
    vernormat.grid(row=12, column=1)
    botaovern = ttk.Button(
        page2,
        text='Verificação da norma',
        command=vernorma
    )
    botaovern.grid(row=12, column=2)

    # calculando a area do aço

    labelnumbarras = tk.Label(page2,
                              text='Calculando o numero de barras:',
                              font=('Arial', 10)
                              )
    labelnumbarras.grid(row=13, column=1)

    def Areaaco():
        global Asp
        global Asmin
        Fyd = cavalor / 1.15
        Asp = valormd * 100 / (Fyd * (d - 0.4 * lnvalor))
        Asmin = 0.15 * d
        if Asmin > Asp:
            areaacot.configure(state='normal')
            areaacot.delete('1.0', 'end')
            areaacot.insert('1.0', Asmin)

            areaacot.configure(state='disabled')
        else:
            areaacot.configure(state='normal')
            areaacot.delete('1.0', 'end')
            areaacot.insert('1.0', Asp)

            areaacot.configure(state='disabled')

    labelareaaco = tk.Label(page2,
                            text='Area do aço (cm2):',
                            font=('Arial', 10)
                            )
    areaacot = Text(page2, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelareaaco.grid(row=14, column=0)
    areaacot.grid(row=14, column=1)
    botaoasp = ttk.Button(
        page2,
        text='ok!',
        command=Areaaco
    )
    botaoasp.grid(row=14, column=2)


    # calculo da barra principal

    # armazenando valor da bitola escolhida
    labelbit = tk.Label(page2,
                        text='bitola do aço (mm):',
                        font=('Arial', 10)
                        )
    bit = Text(page2,  width=50, height=1, bd=3, relief='sunken')
    bit.insert("1.0", "Digite o valor da bitola do aço que você deseja")
    labelbit.grid(row=15, column=0)
    bit.bind('<Button-1>', clear_text)
    bit.grid(row=15, column=1)

    def valorbit():
        global bitvalor
        bitvalor = bit.get('1.0', 'end')
        bitvalor = float(bitvalor)

    botaobit = ttk.Button(
        page2,
        text='ok!',
        command=valorbit
    )
    botaobit.grid(row=15, column=2)

    def numferros():
        global Abitp
        global Numferros
        global Ah
        global av
        global Ncadacam
        global Ncamadas
        global Nultimacamada
        Abitp = mt.pi * ((bitvalor / 10) ** 2) / 4
        Numferros = mt.ceil(Asp / Abitp)
        ah1 = 2
        ah2 = bitvalor / 10
        ah3 = 1.2 * 1.9
        Ah = max(ah1, ah2, ah3)
        av1 = 2
        av2 = bitvalor / 10
        av3 = 0.5 * 1.9
        av = max(av1, av2, av3)
        Ncad = hvalor + Ah - 2 * cvalor - 2 * fitvalor
        Ncad2 = Ah + (bitvalor / 10)
        Ncadacam = int(Ncad / Ncad2)
        Ncamadas = mt.ceil(Numferros / Ncadacam)
        Nultimacamada = Numferros % Ncadacam

        numferrost.configure(state='normal')
        numferrost.delete('1.0', 'end')
        numferrost.insert('1.0', 'N01 D/: {}'.format(Numferros))
        numferrost.configure(state='disabled')

        Aht.configure(state='normal')
        Aht.delete('1.0', 'end')
        Aht.insert('1.0', 'O espaçamento horizontal é {}'.format(Ah))

        Aht.configure(state='disabled')


        avt.configure(state='normal')
        avt.delete('1.0', 'end')
        avt.insert('1.0', 'O espaçamento vertical é {}'.format(av))

        avt.configure(state='disabled')

        Ncadacamt.configure(state='normal')
        Ncadacamt.delete('1.0', 'end')
        Ncadacamt.insert('1.0', 'O Nº de barras em cada camada é {}'.format(Ncadacam))

        Ncadacamt.configure(state='disabled')

        Ncamadast.configure(state='normal')
        Ncamadast.delete('1.0', 'end')
        Ncamadast.insert('1.0', 'O Nº de camadas é {}'.format(Ncamadas))

        Ncamadast.configure(state='disabled')

        Nultimacamadat.configure(state='normal')
        Nultimacamadat.delete('1.0', 'end')
        Nultimacamadat.insert('1.0', 'O Nº de barras na última camada é {}'.format(Nultimacamada))

        Nultimacamadat.configure(state='disabled')

    labelnum = tk.Label(page2,
                        text='Numero de barras:',
                        font=('Arial', 10)
                        )
    numferrost = Text(page2, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelnum.grid(row=16, column=0)
    numferrost.grid(row=16, column=1)
    botaonum = ttk.Button(
        page2,
        text='numferros',
        command=numferros
    )
    botaonum.grid(row=16, column=2)

    labelAh = tk.Label(page2,
                        text='Ah:',
                        font=('Arial', 10)
                        )
    Aht = Text(page2, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelAh.grid(row=17, column=0)
    Aht.grid(row=17, column=1)

    labelav = tk.Label(page2,
                       text='Av:',
                       font=('Arial', 10)
                       )
    avt = Text(page2,  width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelav.grid(row=18, column=0)
    avt.grid(row=18, column=1)

    labelncadcam = tk.Label(page2,
                       text='Nº B/ em cada camada:',
                       font=('Arial', 10)
                       )
    Ncadacamt = Text(page2,  width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelncadcam.grid(row=19, column=0)
    Ncadacamt.grid(row=19, column=1)


    labelncamadas = tk.Label(page2,
                            text='Nº de camadas:',
                            font=('Arial', 10)
                            )
    Ncamadast = Text(page2,  width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelncamadas.grid(row=20, column=0)
    Ncamadast.grid(row=20, column=1)


    labelnultimacamada = tk.Label(page2,
                             text='Nº B/ na ultima camada:',
                             font=('Arial', 10)
                             )
    Nultimacamadat = Text(page2,  width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelnultimacamada.grid(row=21, column=0)
    Nultimacamadat.grid(row=21, column=1)

    # automação do cad

    def Autocad():
        global descram
        descram = descramcombo.get()
        if descram == 'sim':
            # Desenho automatico no autocad
            # Montando forma (quadrado de fora):
            with open("Viga.scr", "w") as arquivo:
                # variaveis
                interb = (hvalor - 2 * cvalor) + cvalor
                interh = (alturavalor - 2 * cvalor) + cvalor 
                interfit = cvalor + fitvalor 
                interbt = interb - 1 * fitvalor
                interht = interh - 1 * fitvalor
                rcircle = (bitvalor / 10) / 2
                posicb = interfit + rcircle
                posich = interfit + rcircle

                arquivo.write("_RECTANGLE\n")
                arquivo.write("0,0\n")
                arquivo.write(f"{hvalor},{alturavalor}\n")
            # Montando ferragem (quadrados de dentro)
                arquivo.write("_RECTANGLE\n")
                arquivo.write(f"{cvalor},{cvalor}\n")
                arquivo.write(f"{interb},{interh}\n")
                arquivo.write("_RECTANGLE\n")
                arquivo.write(f"{interfit},{interfit}\n")
                arquivo.write(f"{interbt},{interht}\n")

            # bitolas (circulos da primeira camada por enquanto)
                for u in range(Ncadacam):
                    arquivo.write("_CIRCLE\n")
                    arquivo.write(f"{posicb},{posich}\n")
                    arquivo.write(f"{rcircle}\n")
                    posicb = Ah + posicb + (bitvalor / 10)
                if Ncamadas == 2:
                    if Nultimacamada == 0:
                        posich = (av) + posich + (bitvalor / 10)
                        posicb = interfit + rcircle
                        for o in range(Ncadacam):
                            arquivo.write("_CIRCLE\n")
                            arquivo.write(f"{posicb},{posich}\n")
                            arquivo.write(f"{rcircle}\n")
                            posicb = Ah + posicb + (bitvalor / 10)
                    elif Nultimacamada != 0:
                        posich = av + posich + (bitvalor / 10)
                        posicb = interfit + rcircle
                        for o in range(Nultimacamada):
                            arquivo.write("CIRCLE\n")
                            arquivo.write(f"{posicb},{posich}\n")
                            arquivo.write(f"{rcircle}\n")
                            posicb = Ah + posicb + (bitvalor / 10)
                if Ncamadas >= 3:
                    if Nultimacamada == 0:
                        for n in range(Ncamadas - 1):
                            posich = av + posich + (bitvalor / 10)
                            posicb = interfit + rcircle
                            for o in range(Ncadacam):
                                arquivo.write("CIRCLE\n")
                                arquivo.write(f"{posicb},{posich}\n")
                                arquivo.write(f"{rcircle}\n")
                                posicb = Ah + posicb + (bitvalor / 10)
                    elif Nultimacamada != 0:
                        for n in range(Ncamadas - 2):
                            posich = av + posich + (bitvalor / 10)
                            posicb = interfit + rcircle
                            for o in range(Ncadacam):
                                arquivo.write("CIRCLE\n")
                                arquivo.write(f"{posicb},{posich}\n")
                                arquivo.write(f"{rcircle}\n")
                                posicb = Ah + posicb + (bitvalor / 10)
                        posich = av + posich + (bitvalor / 10)
                        posicb = interfit + rcircle
                        for o in range(Nultimacamada):
                            arquivo.write("CIRCLE\n")
                            arquivo.write(f"{posicb},{posich}\n")
                            arquivo.write(f"{rcircle}\n")
                            posicb = Ah + posicb + (bitvalor / 10)
        else:
            print("fim")
    # armazenando automação

    labeldescram = ttk.Label(page2,
                        text='Deseja desenhar automaticamnte no autocad?',
                        font=('Arial', 10)
                        )
    descram = ['sim', 'não']
    descramcombo = ttk.Combobox(page2,  values=descram)
    labeldescram.grid(row=22, column=0)
    descramcombo.grid(row=22, column=1)
    botaodescram = ttk.Button(
        page2,
        text='ok!',
        command=Autocad
        )
    botaodescram.grid(row=22, column=2)
    def voltar_para_root():

        VigaNewindow.destroy()
        root.deiconify()

    return_button = tk.Button(frame, text='Voltar', command=voltar_para_root)
    return_button.grid(row=25, column=0, padx=5, pady=7)
    root.withdraw()
    VigaNewindow.protocol("WM_DELETE_WINDOW", fechar_janela)
    VigaNewindow.update()
    canvas.config(scrollregion=canvas.bbox('all'))
    







    root.withdraw()
    VigaNewindow.protocol("WM_DELETE_WINDOW", fechar_janela)


root.mainloop()

E = 70*10**3
b = 40
h = 80
A = b*h
I = b * (h**3)/12
theta = float(input("digite o angulo de inclinação da viga"))
L = float(input("digite o comprimento da viga"))
c = sp.cos(theta)
s = sp.sin(theta)
#Matriz de rigidez local do elemento
ke_ = np.array([
    [E*A/L, 0, 0, -E*A/L, 0, 0],
    [0, 12*E*I/(L**3), 6*E*I/(L**2), 0, -12*E*I/(L**3), 6*E*I/(L**2)],
    [0, 6*E*I/(L**2), 4*E*I/L, 0, -6*E*I/(L**2), 2*E*I/L],
    [-E*A/L, 0, 0, E*A/L, 0, 0],
    [0, -12*E*I/(L**3), -6*E*I/(L**2), 0, 12*E*I/(L**3), -6*E*I/(L**2)],
    [0, 6*E*I/(L**2), 2*E*I/L, 0, -6*E*I/(L**2), 4*E*I/L]
])
#Matriz de rigidez global do elemento

T = sp.Matrix([
    [c, -s, 0, 0, 0, 0],
    [s, c, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, c, -s, 0],
    [0, 0, 0, s, c, 0],
    [0, 0, 0, 0, 0, 1]
]).T
Ke = T.T * ke_ * T
