import math as mt
import tkinter as tk
import numpy as np
import sympy as sp
from tkinter import *
from tkinter import ttk, Text
from ttkbootstrap import Style
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import zip_longest, chain

def abrir_janela():
    opcao = comboboxinicio.get()
    if opcao == "Rampa":
        RampaNewWindow(opcao)
    elif opcao == "Escada":
        EscadaNewWindow(opcao)
    else:
        VigaNewWindow(opcao)
def fechar_janela():
    root.destroy()



# Janela principal
root = tk.Tk()
style = Style(theme = 'yeti')
root = style.master
root.geometry("1025x650")
root.title('Pystruct')
#root.geometry("Expansive")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)


# opções do combobox
val = ['Rampa', 'Escada', 'Viga']

#Criação do Combobox
comboboxinicio = ttk.Combobox(root, values=val)
comboboxinicio.place(x=430, y=370)

# Texto de seleção
T1 = ttk.Label(
    text='BEM VINDO AO PYSTRUCT!',
    font=('Arial', 30)


)
T1.grid(row=0, column=1)

# Texto de seleção
T2 = ttk.Label(
    text='Qual estrutura voce gostaria de dimensionar?',
    font=('Arial', 10)


)
T2.grid(row=1, column=1)
# botão de seleção
B1 = ttk.Button(
    root,
    text='Selecionar',
    command=abrir_janela
)

B1.place(x=465, y=410)


# criação das janelas com as opções a serem dimensionadas
#janela da estrutura Rampa
def RampaNewWindow(opcao):
    #caracterisitcas da Janela nova
    RampaNewWindow = tk.Toplevel()
    RampaNewWindow.title(opcao)
    RampaNewWindow.geometry("825x650")
    # criando barra de rolagem
    barra = Scrollbar(RampaNewWindow)
    canvas = Canvas(RampaNewWindow, yscrollcommand = barra.set)
    barra.config(command=canvas.yview)
    barra.pack(side='right', fill='y')


    frame = Frame(canvas)
    canvas.pack(side='top', fill='both', expand=True)
    canvas.create_window(0,0, window=frame)
    #apagando o texto ao clicar
    def clear_text(event):
        event.widget.delete('1.0', tk.END)

    #conteudo da janela nova

    label = tk.Label(frame,
    text = 'Calculando valor de alfa:',
    font = ('Arial', 10)
    )
    label.grid(row=0, column=1)


    # armazenando distância vertical

    labelv = tk.Label(frame,
        text = 'V (m):',
        font = ('Arial', 10)
    )
    v = Text(frame, width=50, height=1, bd=3, relief='sunken')
    v.insert("1.0", "Digite o valor da distância vertical da rampa")
    labelv.grid(row=1, column=0)
    v.bind('<Button-1>', clear_text)
    v.grid(row=1, column=1)

    def valorv():
        global vvalor
        vvalor = v.get('1.0', 'end')
        vvalor = float(vvalor)


    botaov = ttk.Button(
        frame,
        text='ok!',
        command=valorv
    )
    botaov.grid(row=1, column=2)

    # armazenando distância horizontal
    labelh = tk.Label(frame,
                      text='H (m):',
                      font=('Arial', 10)
                      )
    h = Text(frame, width=50, height=1, bd=3, relief='sunken')
    h.insert("1.0", "Digite o valor da distância horizontal da rampa")
    labelh.grid(row=2, column=0)
    h.bind('<Button-1>', clear_text)
    h.grid(row=2, column=1)

    def valorh():
        global hvalor
        hvalor = h.get('1.0', 'end')
        hvalor = float(hvalor)

    botaoh = ttk.Button(
        frame,
        text='ok!',
        command=valorh
    )
    botaoh.grid(row=2, column=2)



    #armazenando valor da altura

    labelaltura = tk.Label(frame,
                       text='Altura (m):',
                       font=('Arial', 10)
                       )
    altura = Text(frame, width=50, height=1, bd=3, relief='sunken')
    altura.insert("1.0", "Digite o valor da altura da rampa")
    labelaltura.grid(row=3, column=0)
    altura.bind('<Button-1>', clear_text)
    altura.grid(row=3, column=1)

    def valoraltura():
        global alturavalor
        alturavalor = altura.get('1.0', 'end')
        alturavalor = float(alturavalor)

    botaoaltura = ttk.Button(
        frame,
        text='ok!',
        command=valoraltura
    )
    botaoaltura.grid(row=3, column=2)




    # Saída com valor de alfa calculado

    def valoralfa():
        global inclinacao
        global Alfa
        inclinacao = vvalor / hvalor
        Alfa = mt.atan(inclinacao)
        al.configure(state='normal')
        al.delete('1.0', 'end')
        Alfa = mt.degrees(Alfa)
        al.insert('1.0', Alfa)


        al.configure(state='disabled')


    labelal = tk.Label(frame,
                       text='Alfa:',
                       font=('Arial', 10)
                       )
    al = Text(frame, width=50, height=1, bd=3, relief='sunken', state = 'disabled')
    labelal.grid(row=4, column=0)
    al.grid(row=4, column=1)


    botaoalfa = ttk.Button(
        frame,
        text = 'calcular alfa',
        command=valoralfa

    )
    botaoalfa.grid (row=4, column=2)

    # Saída com valor de altura util calculada

    def valoralturautil():
        global hutil
        hutil = alturavalor / mt.cos(Alfa)
        alturautil.configure(state='normal')
        alturautil.delete('1.0', 'end')
        alturautil.insert('1.0', hutil)

        alturautil.configure(state='disabled')

    labelalturautil = tk.Label(frame,
                       text='Altura útil (m):',
                       font=('Arial', 10)
                       )
    alturautil = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelalturautil.grid(row=5, column=0)
    alturautil.grid(row=5, column=1)

    botaoalturautil = ttk.Button(
        frame,
        text='calcular altura útil',
        command=valoralturautil

    )
    botaoalturautil.grid(row=5, column=2)


    # carregamentos

    label = tk.Label(frame,
                     text='Calculando valor dos carregamentos:',
                     font=('Arial', 10)
                     )
    label.grid(row=6, column=1)


    # armazenando dimensôes do cobrimento
    labelc = tk.Label(frame,
                      text='c (cm):',
                      font=('Arial', 10)
                      )
    c = Text(frame, width=50, height=1, bd=3, relief='sunken')
    c.insert("1.0", "Digite o valor do cobrimento")
    labelc.grid(row=7, column=0)
    c.bind('<Button-1>', clear_text)
    c.grid(row=7, column=1)

    def valorc():
        global cvalor
        cvalor = c.get('1.0', 'end')
        cvalor = float(cvalor)

    botaoc = ttk.Button(
        frame,
        text='ok!',
        command=valorc
    )
    botaoc.grid(row=7, column=2)

    # armazenando a resistência do aço
    labelca = tk.Label(frame,
                       text='CA (Kgf/mm2):',
                       font=('Arial', 10)
                       )
    ca = Text(frame, width=50, height=1, bd=3, relief='sunken')
    ca.insert("1.0", "Digite o valor da resistência do aço")
    labelca.grid(row=8, column=0)
    ca.bind('<Button-1>', clear_text)
    ca.grid(row=8, column=1)

    def valorca():
        global cavalor
        cavalor = ca.get('1.0', 'end')
        cavalor = float(cavalor)

    botaoca = ttk.Button(
        frame,
        text='ok!',
        command=valorca
    )
    botaoca.grid(row=8, column=2)

    # armazenando valor de Fck
    labelFck = tk.Label(frame,
                      text='Fck (Mpa):',
                      font=('Arial', 10)
                      )
    Fck = Text(frame, width=50, height=1, bd=3, relief='sunken')
    Fck.insert("1.0", "Digite o valor do Fck")
    labelFck.grid(row=9, column=0)
    Fck.bind('<Button-1>', clear_text)
    Fck.grid(row=9, column=1)

    def valorFck():
        global Fckvalor
        Fckvalor = Fck.get('1.0', 'end')
        Fckvalor = float(Fckvalor)

    botaoFck = ttk.Button(
        frame,
        text='ok!',
        command=valorFck
    )
    botaoFck.grid(row=9, column=2)

    # armazenando a carga de revestimento
    labelrev = ttk.Label(frame,
                       text='Rev (KN):',
                       font=('Arial', 10)
                       )
    rev = Text(frame, width=50, height=1, bd=3, relief='sunken')
    rev.insert("1.0", "Digite o valor do revestimento")
    labelrev.grid(row=10, column=0)
    rev.bind('<Button-1>', clear_text)
    rev.grid(row=10, column=1)

    def valorrev():
        global revvalor
        revvalor = rev.get('1.0', 'end')
        revvalor = float(revvalor)

    botaorev = ttk.Button(
        frame,
        text='ok!',
        command=valorrev
    )
    botaorev.grid(row=10, column=2)

    #calculando momento

    def valormomento():
        global P
        global valorMd

        PP = (hutil / 100) * 25
        P = (PP + revvalor) * 1.4
        valorMd = ((P * (hvalor ** 2)) / 8) + ((100 * 1.4 * (hvalor / 2) ** 2) / hvalor)

        Md.configure(state='normal')
        Md.delete('1.0', 'end')
        Md.insert('1.0', valorMd)

        Md.configure(state='disabled')

    labelMd = tk.Label(frame,
                       text='Momento (KN/m2):',
                       font=('Arial', 10)
                       )
    Md = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelMd.grid(row=11, column=0)
    Md.grid(row=11, column=1)

    botaoMd = ttk.Button(
        frame,
        text='calcular Momento',
        command=valormomento

    )
    botaoMd.grid(row=11, column=2)

    # Calculando a linha neutra

    def valorlinhaneutra():
        global d
        global Fcd
        fil = 1
        Fcd = (Fckvalor / 1.4) / 10
        d = hutil - cvalor - (fil / 2)
        a = 0.68 * 0.4 * Fcd * 100
        b = - 0.68 * Fcd * d * 100
        C = valorMd * 100
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

    labelln = tk.Label(frame,
                       text='Linha neutra (ln):',
                       font=('Arial', 10)
                       )
    ln = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelln.grid(row=12, column=0)
    ln.grid(row=12, column=1)

    botaoln = ttk.Button(
                frame,
                text='calcular linha neutra',
                command=valorlinhaneutra

                    )
    botaoln.grid(row=12, column=2)
    def vernorma():
        vernorma = lnvalor/d
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

    labelvern = tk.Label(frame,
                       text='Verificação da norma:',
                       font=('Arial', 10)
                       )
    vernormat = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelvern.grid(row=13, column=0)
    vernormat.grid(row=13, column=1)
    botaovern = ttk.Button(
        frame,
        text='Verificação da norma',
        command=vernorma
    )
    botaovern.grid(row=13, column=2)


    #calculando a area do aço

    labelnumbarras = tk.Label(frame,
                     text='Calculando o numero de barras:',
                     font=('Arial', 10)
                     )
    labelnumbarras.grid(row=14, column=1)


    def Areaaco():
        global Asp
        global Asmin
        Fyd = cavalor / 1.15
        Asp = valorMd * 100 / (Fyd * (d - 0.4 * lnvalor))
        Asmin = 0.15 * d
        if Asmin > Asp:
            areaacot.configure(state='normal')
            areaacot.delete('1.0', 'end')
            areaacot.insert('1.0', 'Viga não permitida')

            areaacot.configure(state='disabled')
        else:
            areaacot.configure(state='normal')
            areaacot.delete('1.0', 'end')
            areaacot.insert('1.0', Asp)

            areaacot.configure(state='disabled')

    labelareaaco = tk.Label(frame,
                         text='Area do aço: (cm2)',
                         font=('Arial', 10)
                         )
    areaacot = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelareaaco.grid(row=15, column=0)
    areaacot.grid(row=15, column=1)
    botaoasp = ttk.Button(
        frame,
        text='Area do aço',
        command=Areaaco
    )
    botaoasp.grid(row=15, column=2)

    #calculo da barra principal

    # armazenando valor da bitola escolhida
    labelbit = tk.Label(frame,
                        text='bitola do aço (mm):',
                        font=('Arial', 10)
                        )
    bit = Text(frame, width=50, height=1, bd=3, relief='sunken')
    bit.insert("1.0", "Digite o valor da bitola do aço que você deseja ")
    labelbit.grid(row=16, column=0)
    bit.bind('<Button-1>', clear_text)
    bit.grid(row=16, column=1)

    def valorbit():
        global bitvalor
        bitvalor = bit.get('1.0', 'end')
        bitvalor = float(bitvalor)

    botaobit = ttk.Button(
        frame,
        text='ok!',
        command=valorbit
    )
    botaobit.grid(row=16, column=2)
    def numferros():
        global Abitp
        Abitp = mt.pi * ((bitvalor / 10) ** 2) / 4
        Numferros = mt.ceil(Asp / Abitp)
        Esp1 = 100 / Numferros
        if Esp1 > 20:
            numferrost.configure(state='normal')
            numferrost.delete('1.0', 'end')
            numferrost.insert('1.0', 'Espaçamento não permitido')

            numferrost.configure(state='disabled')
        elif Esp1 > 2 * hvalor:
            numferrost.configure(state='normal')
            numferrost.delete('1.0', 'end')
            numferrost.insert('1.0', 'Espaçamento não permitido')

            numferrost.configure(state='disabled')
        else:
            numferrost.configure(state='normal')
            numferrost.delete('1.0', 'end')
            numferrost.insert('1.0', 'N01 D/: {},c/ {}'.format(Numferros, Esp1))

            numferrost.configure(state='disabled')

    labelnum = tk.Label(frame,
                            text='Numero de barras:',
                            font=('Arial', 10)
                            )
    numferrost = Text(frame, width=50, height=1, bd=3, relief='sunken')
    labelnum.grid(row=17, column=0)
    numferrost.grid(row=17, column=1)
    botaonum = ttk.Button(
        frame,
        text='numferros',
        command=numferros
    )
    botaonum.grid(row=17, column=2)


    #calculando a barra secundária

    labelnumbarras2 = tk.Label(frame,
                              text='Calculando o numero de barras secundárias:',
                              font=('Arial', 10)
                              )
    labelnumbarras2.grid(row=18, column=1)


    def valornumbit2():
        global Numdbits2
        Numdbits2 = bit.get('1.0', 'end')
        Numdbits2 = float(Numdbits2)



    labeldbits2 = tk.Label(frame,
                         text='Digite o valor da bitola do aço que você deseja (mm):',
                         font=('Arial', 10)
                         )
    numdbits2 = Text(frame, width=50, height=1, bd=3, relief='sunken')
    labeldbits2.grid(row=19, column=0)
    numdbits2.grid(row=19, column=1)
    botaonumdbits2 = ttk.Button(
        frame,
        text='ok!',
        command=valornumbit2
    )
    botaonumdbits2.grid(row=19, column=2)


    def numferros2():
        Asdis1 = 0.2 * Asp
        Asdis2 = 0.5 * Asmin
        Asdis = max(Asdis1, Asdis2, 0.9)
        Abits = mt.pi * ((Numdbits2 / 10) ** 2) / 4
        Numferros2 = mt.ceil(Asdis / Abits)
        Ssec = 100 / Numferros2
        if Ssec > 33:
            numferrost2.configure(state='normal')
            numferrost2.delete('1.0', 'end')
            numferrost2.insert('1.0', 'Barra não permitida')

            numferrost2.configure(state='disabled')
        else:
            numferrost2.configure(state='normal')
            numferrost2.delete('1.0', 'end')
            numferrost2.insert('1.0', 'N01 D/: {},c/ {}'.format(Numferros2, Ssec))

            numferrost2.configure(state='disabled')

    labelnum2 = tk.Label(frame,
                            text='Numero de barras:',
                            font=('Arial', 10)
                            )
    numferrost2 = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelnum2.grid(row=20, column=0)
    numferrost2.grid(row=20, column=1)
    botaonum2 = ttk.Button(
            frame,
            text='numferros2',
            command=numferros2
        )
    botaonum2.grid(row=20, column=2)

    def voltar_para_root():

        RampaNewWindow.destroy()
        root.deiconify()

    return_button = tk.Button (frame, text= 'Voltar', command=voltar_para_root)
    return_button.grid(row=21, column=0, padx=5, pady= 7)

    






    # funcionalidades de fechamento e abertura da janela nova
    root.withdraw()
    RampaNewWindow.protocol("WM_DELETE_WINDOW", fechar_janela)
    RampaNewWindow.update()
    canvas.config(scrollregion=canvas.bbox('all'))





# janela da estrutura Escada
def EscadaNewWindow(opcao):
    EscadaNewindow = tk.Toplevel()
    EscadaNewindow.title(opcao)
    EscadaNewindow.geometry("825x650")
    # criando barra de rolagem
    barra = Scrollbar(EscadaNewindow)
    canvas = Canvas(EscadaNewindow, yscrollcommand = barra.set)
    barra.config(command=canvas.yview)
    barra.pack(side='right', fill='y')


    frame = Frame(canvas)
    canvas.pack(side='top', fill='both', expand=True)
    canvas.create_window(0,0, window=frame)
    # conteudo da janela nova

    label = tk.Label(frame,
                     text='Calculando valor de alfa:',
                     font=('Arial', 10)
                     )
    label.grid(row=0, column=1)

    # Apagando o conteúdo
    def clear_text(event):
        event.widget.delete('1.0', tk.END)

    # armazenando distância vertical

    labelv = tk.Label(frame,
                      text='V (m):',
                      font=('Arial', 10)
                      )
    v = Text(frame, width=50, height=1, bd=3, relief='sunken')
    v.insert("1.0", "Digite o valor da distância vertical da escada")
    labelv.grid(row=1, column=0)
    v.bind('<Button-1>', clear_text)
    v.grid(row=1, column=1)

    def valorv():
        global vvalor
        vvalor = v.get('1.0', 'end')
        vvalor = vvalor.strip()
        vvalor = float(vvalor)

    botaov = ttk.Button(
        frame,
        text='ok!',
        command=valorv
    )
    botaov.grid(row=1, column=2)

    # armazenando distância horizontal
    labelh = tk.Label(frame,
                      text='H (m):',
                      font=('Arial', 10)
                      )
    h = Text(frame, width=50, height=1, bd=3, relief='sunken')
    h.insert("1.0", "Digite o valor da distância horizontal da escada")
    labelh.grid(row=2, column=0)
    h.bind('<Button-1>', clear_text)
    h.grid(row=2, column=1)

    def valorh():
        global hvalor
        hvalor = h.get('1.0', 'end')
        hvalor = float(hvalor)

    botaoh = ttk.Button(
        frame,
        text='ok!',
        command=valorh
    )
    botaoh.grid(row=2, column=2)

    # armazenando valor do espelho
    labele = tk.Label(frame,
                      text='e (cm):',
                      font=('Arial', 10)
                      )
    e = Text(frame, width=50, height=1, bd=3, relief='sunken')
    e.insert("1.0", "Digite o valor do espelho da escada")
    labele.grid(row=3, column=0)
    e.bind('<Button-1>', clear_text)
    e.grid(row=3, column=1)

    def valore():
        global evalor
        evalor = e.get('1.0', 'end')
        evalor = float(evalor)

    botaoe = ttk.Button(
        frame,
        text='ok!',
        command=valore
    )
    botaoe.grid(row=3, column=2)

    # armazenando valor do piso
    labels = tk.Label(frame,
                      text='s (cm):',
                      font=('Arial', 10)
                      )
    s = Text(frame, width=50, height=1, bd=3, relief='sunken')
    s.insert("1.0", "Digite o valor do piso da escada")
    labels.grid(row=4, column=0)
    s.bind('<Button-1>', clear_text)
    s.grid(row=4, column=1)

    def valors():
        global svalor
        svalor = s.get('1.0', 'end')
        svalor = float(svalor)

    botaos = ttk.Button(
        frame,
        text='ok!',
        command=valors
    )
    botaos.grid(row=4, column=2)





    # armazenando valor da altura

    labelaltura = tk.Label(frame,
                           text='Altura (m):',
                           font=('Arial', 10)
                           )
    altura = Text(frame, width=50, height=1, bd=3, relief='sunken')
    altura.insert("1.0", "Digite o valor da altura da escada")
    labelaltura.grid(row=5, column=0)
    altura.bind('<Button-1>', clear_text)
    altura.grid(row=5, column=1)

    def valoraltura():
        global alturavalor
        alturavalor = altura.get('1.0', 'end')
        alturavalor = float(alturavalor)

    botaoaltura = ttk.Button(
        frame,
        text='ok!',
        command=valoraltura
    )
    botaoaltura.grid(row=5, column=2)

    # Saída com valor de alfa calculado

    def valoralfa():
        global Alfa
        Alfa = mt.atan(evalor / svalor)
        al.configure(state='normal')
        al.delete('1.0', 'end')
        Alfa = mt.degrees(Alfa)
        al.insert('1.0', Alfa)

        al.configure(state='disabled')

    labelal = tk.Label(frame,
                       text='Alfa:',
                       font=('Arial', 10)
                       )
    al = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelal.grid(row=6, column=0)
    al.grid(row=6, column=1)

    botaoalfa = ttk.Button(
        frame,
        text='calcular alfa',
        command=valoralfa

    )
    botaoalfa.grid(row=6, column=2)

    # Saída com valor de altura util calculada

    def valoralturautil():
        global hutil
        hutil = alturavalor / mt.cos(Alfa)
        alturautil.configure(state='normal')
        alturautil.delete('1.0', 'end')
        alturautil.insert('1.0', hutil)

    def valorhm():
        global hm
        hm = hutil + (evalor / 2)
        hmt.configure(state='disabled')
        hmt.configure(state='normal')
        hmt.delete('1.0', 'end')
        hmt.insert('1.0', hm)

        hmt.configure(state='disabled')


    labelalturautil = tk.Label(frame,
                               text='Altura útil (h1):',
                               font=('Arial', 10)
                               )
    alturautil = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelalturautil.grid(row=7, column=0)
    alturautil.grid(row=7, column=1)

    botaoalturautil = ttk.Button(
        frame,
        text='calcular altura útil',
        command=valoralturautil

    )
    botaoalturautil.grid(row=7, column=2)

    labelhmt = tk.Label(frame,
                        text='Altura útil (hm):',
                        font=('Arial', 10)
                        )
    hmt = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelhmt.grid(row=8, column=0)
    hmt.grid(row=8, column=1)

    botaohmt = ttk.Button(
        frame,
        text='calcular altura útil m',
        command=valorhm

    )
    botaohmt.grid(row=8, column=2)

    # carregamentos

    label = tk.Label(frame,
                     text='Calculando valor dos carregamentos:',
                     font=('Arial', 10)
                     )
    label.grid(row=9, column=1)




    # armazenando dimensôes do cobrimento
    labelc = tk.Label(frame,
                      text='c (cm):',
                      font=('Arial', 10)
                      )
    c = Text(frame, width=50, height=1, bd=3, relief='sunken')
    c.insert("1.0", "Digite o valor do cobrimento")
    labelc.grid(row=10, column=0)
    c.bind('<Button-1>', clear_text)
    c.grid(row=10, column=1)

    def valorc():
        global cvalor
        cvalor = c.get('1.0', 'end')
        cvalor = float(cvalor)

    botaoc = ttk.Button(
        frame,
        text='ok!',
        command=valorc
    )
    botaoc.grid(row=10, column=2)

    # armazenando a resistência do aço
    labelca = tk.Label(frame,
                       text='CA (kgf/mm2):',
                       font=('Arial', 10)
                       )
    ca = Text(frame, width=50, height=1, bd=3, relief='sunken')
    ca.insert("1.0", "Digite o valor da resistência do aço")
    labelca.grid(row=11, column=0)
    ca.bind('<Button-1>', clear_text)
    ca.grid(row=11, column=1)

    def valorca():
        global cavalor
        cavalor = ca.get('1.0', 'end')
        cavalor = float(cavalor)

    botaoca = ttk.Button(
        frame,
        text='ok!',
        command=valorca
    )
    botaoca.grid(row=11, column=2)

    # armazenando valor de Fck
    labelFck = tk.Label(frame,
                        text='Fck (Mpa):',
                        font=('Arial', 10)
                        )
    Fck = Text(frame, width=50, height=1, bd=3, relief='sunken')
    Fck.insert("1.0", "Digite o valor do Fck")
    labelFck.grid(row=12, column=0)
    Fck.bind('<Button-1>', clear_text)
    Fck.grid(row=12, column=1)

    def valorFck():
        global Fckvalor
        Fckvalor = Fck.get('1.0', 'end')
        Fckvalor = float(Fckvalor)

    botaoFck = ttk.Button(
        frame,
        text='ok!',
        command=valorFck
    )
    botaoFck.grid(row=12, column=2)

    # armazenando a carga de revestimento
    labelrev = ttk.Label(frame,
                         text='Rev (KN):',
                         font=('Arial', 10)
                         )
    rev = Text(frame, width=50, height=1, bd=3, relief='sunken')
    rev.insert("1.0", "Digite o valor do revestimento")
    labelrev.grid(row=13, column=0)
    rev.bind('<Button-1>', clear_text)
    rev.grid(row=13, column=1)

    def valorrev():
        global revvalor
        revvalor = rev.get('1.0', 'end')
        revvalor = float(revvalor)

    botaorev = ttk.Button(
        frame,
        text='ok!',
        command=valorrev
    )
    botaorev.grid(row=13, column=2)

    # armazenando valor do acesso
    def Passeiovalor():
        global passeiovalor
        passeiovalor = passeiocombo.get()
        if passeiovalor == 'sim':
            passeiovalor = float(3)
        else:
            passeiovalor = float(2.5)

    labelpass = ttk.Label(frame,
                         text='A escada possui acesso?',
                         font=('Arial', 10)
                         )
    optionsp = ['sim', 'não']
    passeiocombo = ttk.Combobox(frame, values = optionsp)
    passeiocombo.grid(row=14, column=1)
    labelpass.grid(row=14, column=0)
    botaopasseio = ttk.Button(
        frame,
        text='ok!',
        command=Passeiovalor
    )
    botaopasseio.grid(row=14, column=2)

    # calculando momento

    def valormomento():
        global P
        global valorMd

        PP = (hutil / 100) * 25
        P = (PP + revvalor + passeiovalor) * 1.4
        valorMd = (P * (hvalor ** 2)) / 8

        Md.configure(state='normal')
        Md.delete('1.0', 'end')
        Md.insert('1.0', valorMd)

        Md.configure(state='disabled')

    labelMd = tk.Label(frame,
                       text='Momento (KN/m2):',
                       font=('Arial', 10)
                       )
    Md = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelMd.grid(row=15, column=0)
    Md.grid(row=15, column=1)

    botaoMd = ttk.Button(
        frame,
        text='calcular Momento',
        command=valormomento

    )
    botaoMd.grid(row=15, column=2)

    # Calculando a linha neutra

    def valorlinhaneutra():
        global d
        global Fcd
        fil = 1
        Fcd = (Fckvalor / 1.4) / 10
        d = hm - cvalor - (fil / 2)
        a = 0.68 * 0.4 * Fcd * 100
        b = - 0.68 * Fcd * d * 100
        C = valorMd * 100
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

    labelln = tk.Label(frame,
                       text='Linha neutra (ln):',
                       font=('Arial', 10)
                       )
    ln = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelln.grid(row=16, column=0)
    ln.grid(row=16, column=1)

    botaoln = ttk.Button(
        frame,
        text='calcular linha neutra',
        command=valorlinhaneutra

    )
    botaoln.grid(row=16, column=2)

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

    labelvern = tk.Label(frame,
                         text='Verificação da norma:',
                         font=('Arial', 10)
                         )
    vernormat = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelvern.grid(row=17, column=0)
    vernormat.grid(row=17, column=1)
    botaovern = ttk.Button(
        frame,
        text='Verificação da norma',
        command=vernorma
    )
    botaovern.grid(row=17, column=2)

    # calculando a area do aço

    labelnumbarras = tk.Label(frame,
                              text='Calculando o numero de barras:',
                              font=('Arial', 10)
                              )
    labelnumbarras.grid(row=18, column=1)

    def Areaaco():
        global Asp
        global Asmin
        Fyd = cavalor / 1.15
        Asp = valorMd * 100 / (Fyd * (d - 0.4 * lnvalor))
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

    labelareaaco = tk.Label(frame,
                            text='Area do aço (cm2):',
                            font=('Arial', 10)
                            )
    areaacot = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelareaaco.grid(row=19, column=0)
    areaacot.grid(row=19, column=1)
    botaoasp = ttk.Button(
        frame,
        text='Area do aço',
        command=Areaaco
    )
    botaoasp.grid(row=19, column=2)

    # calculo da barra principal

    # armazenando valor da bitola escolhida
    labelbit = tk.Label(frame,
                        text='bitola do aço (mm):',
                        font=('Arial', 10)
                        )
    bit = Text(frame, width=50, height=1, bd=3, relief='sunken')
    bit.insert("1.0", "Digite o valor da bitola do aço que você deseja")
    labelbit.grid(row=20, column=0)
    bit.bind('<Button-1>', clear_text)
    bit.grid(row=20, column=1)

    def valorbit():
        global bitvalor
        bitvalor = bit.get('1.0', 'end')
        bitvalor = float(bitvalor)

    botaobit = ttk.Button(
        frame,
        text='ok!',
        command=valorbit
    )
    botaobit.grid(row=20, column=2)

    def numferros():
        global Abitp
        Abitp = mt.pi * ((bitvalor / 10) ** 2) / 4
        Numferros = mt.ceil(Asp / Abitp)
        Esp1 = 100 / Numferros
        if Esp1 > 20:
            numferrost.configure(state='normal')
            numferrost.delete('1.0', 'end')
            numferrost.insert('1.0', 'Espaçamento não permitido')

            numferrost.configure(state='disabled')
        elif Esp1 > 2 * hvalor:
            numferrost.configure(state='normal')
            numferrost.delete('1.0', 'end')
            numferrost.insert('1.0', 'Espaçamento não permitido')

            numferrost.configure(state='disabled')
        else:
            numferrost.configure(state='normal')
            numferrost.delete('1.0', 'end')
            numferrost.insert('1.0', 'N01 D/: {},c/ {}'.format(Numferros, Esp1))

            numferrost.configure(state='disabled')

    labelnum = tk.Label(frame,
                        text='Numero de barras:',
                        font=('Arial', 10)
                        )
    numferrost = Text(frame, width=50, height=1, bd=3, relief='sunken')
    labelnum.grid(row=21, column=0)
    numferrost.grid(row=21, column=1)
    botaonum = ttk.Button(
        frame,
        text='numferros',
        command=numferros
    )
    botaonum.grid(row=21, column=2)

    # calculando a barra secundária

    labelnumbarras2 = tk.Label(frame,
                               text='Calculando o numero de barras secundárias:',
                               font=('Arial', 10)
                               )
    labelnumbarras2.grid(row=22, column=1)

    def valornumbit2():
        global Numdbits2
        Numdbits2 = bit.get('1.0', 'end')
        Numdbits2 = float(Numdbits2)

    labeldbits2 = tk.Label(frame,
                           text='Digite o valor da bitola do aço que você deseja (mm):',
                           font=('Arial', 10)
                           )
    numdbits2 = Text(frame, width=50, height=1, bd=3, relief='sunken')
    labeldbits2.grid(row=23, column=0)
    numdbits2.grid(row=23, column=1)
    botaonumdbits2 = ttk.Button(
        frame,
        text='ok!',
        command=valornumbit2
    )
    botaonumdbits2.grid(row=23, column=2)

    def numferros2():
        Asdis1 = 0.2 * Asp
        Asdis2 = 0.5 * Asmin
        Asdis = max(Asdis1, Asdis2, 0.9)
        Abits = mt.pi * ((Numdbits2 / 10) ** 2) / 4
        Numferros2 = mt.ceil(Asdis / Abits)
        Ssec = 100 / Numferros2
        if Ssec > 33:
            numferrost2.configure(state='normal')
            numferrost2.delete('1.0', 'end')
            numferrost2.insert('1.0', 'Barra não permitida')

            numferrost2.configure(state='disabled')
        else:
            numferrost2.configure(state='normal')
            numferrost2.delete('1.0', 'end')
            numferrost2.insert('1.0', 'N01 D/: {},c/ {}'.format(Numferros2, Ssec))

            numferrost2.configure(state='disabled')

    labelnum2 = tk.Label(frame,
                         text='Numero de barras:',
                         font=('Arial', 10)
                         )
    numferrost2 = Text(frame, width=50, height=1, bd=3, relief='sunken', state='disabled')
    labelnum2.grid(row=24, column=0)
    numferrost2.grid(row=24, column=1)
    botaonum2 = ttk.Button(
        frame,
        text='numferros2',
        command=numferros2
    )
    botaonum2.grid(row=24, column=2)

    def voltar_para_root():

        EscadaNewindow.destroy()
        root.deiconify()

    return_button = tk.Button(frame, text='Voltar', command=voltar_para_root)
    return_button.grid(row=25, column=0, padx=5, pady=7)
    root.withdraw()
    EscadaNewindow.protocol("WM_DELETE_WINDOW", fechar_janela)
    EscadaNewindow.update()
    canvas.config(scrollregion=canvas.bbox('all'))



#janela da estrutura Viga
def VigaNewWindow(opcao):
    VigaNewindow = tk.Toplevel()
    VigaNewindow.title(opcao)
    VigaNewindow.geometry("1025x650")
    

    # criando barra de rolagem
    barra = Scrollbar(VigaNewindow)
    canvas = Canvas(VigaNewindow, yscrollcommand = barra.set)
    barra.config(command=canvas.yview)
    barra.pack(side='right', fill='y')


    frame = Frame(canvas)
    canvas.pack(side='top', fill='both', expand=True)
    canvas.create_window(0,0, window=frame, anchor='nw')

    # Configurar a expansão do frame
    frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

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

    Ke_ = []
    Ke_soma = []
    momentos = []
    beta = []
    
    
    
    
    
    def Valor_momento_1_elemento():
        global momentos_unidos_final
        momentos_unidos_final = []
        global dist_x_reacoes
        dist_x_reacoes = []
        for i in forca_elem1:
            forca_elem.append(float(i.get("1.0", "end-1c")))
        for i in largura_elem1:
            largura_elem.append(float(i.get("1.0", "end-1c")))
        valor_entry = len(forca_elem)
        global momento_simples
        global Ke_simples
        if valor_entry == 1 and passeiocombod.get() == "não" and passeiocomboe.get() == "não":
            momento_simples = (-forca_elem[0] * (largura_elem[0]**2))/8
            momentos_unidos_final.append(momento_simples)
            dist_x_reacoes.append(largura_elem)
        if valor_entry == 2 and passeiocombod.get() == "não" and passeiocomboe.get() == "não":
            momento_barra1dir = -forca_elem[0] * largura_elem[0]**2/8
            momentos.append(momento_barra1dir)
            Ke_simples = (3 * evalor * ivalor)/largura_elem[0]
            Ke_.append(Ke_simples)
            for i in range(1, len(forca_elem) - 1):
                q = forca_elem[i]
                l = largura_elem[i]
                momento = (q * l ** 2) / 12
                Ke = evalor * ivalor * 4 / l
                Ke_.append(Ke)
                Ke_.append(Ke)
                if i % 2 == 0:
                    momentos.append(-momento)
                    momentos.append(momento)
                else:
                    momentos.append(momento)
                    momentos.append(-momento)
            momento_ultima_barraesq = forca_elem[-1] * (largura_elem[-1]**2)/8
            momentos.append(momento_ultima_barraesq)
            Ke_ultimo = (3 * evalor * ivalor)/largura_elem[-1]
            Ke_.append(Ke_ultimo)
            for i in range(0, len(momentos), 2):
                soma = momentos[i] + momentos[i+1]
                beta.append(soma)
                soma_ke = Ke_[i] + Ke_[i+1]
                Ke_soma.append(soma_ke)
                global beta_matriz
                global Ke_matriz
                global D_matriz
                global momentos_2
                global matriz_Ke_final
                global mult_D_K
                global momento_negativo_final
                Ke_matriz = np.diag(Ke_soma)
                Ke_auxiliar = [Ke_[i] for i in range(1,len(Ke_))]
                for i in range(len(Ke_matriz)):
                    for j in range(len(Ke_matriz)):
                        if i == j:
                            continue  # pula a diagonal principal
                        elif abs(i - j) == 1:
                            Ke_matriz[i][j] = Ke_auxiliar[i] / 2  # atualiza elementos com diferença i-j = 1 
                        else:
                            Ke_matriz[i][j] = 0  # zera os demais elementos
                beta2 = np.array([-1 * b for b in beta])
                beta_matriz = np.array([beta2])
                D_matriz_correta = np.linalg.solve(Ke_matriz, beta_matriz.T)
                D_matriz = D_matriz_correta.T
                momentos_2 = momentos.copy()  # copia a lista original
                momentos_2.insert(0, 0)  # adiciona 0 no índice 0
                momentos_2.append(0)  # adiciona 0 no final da lista
                num_D_matriz = D_matriz.shape[1]
                if valor_entry == 3:
                    matriz_Ke_final = np.zeros((num_D_matriz, len(momentos_2)))
                else:
                    matriz_Ke_final = np.zeros((num_D_matriz, len(momentos_2)))  
                if num_D_matriz == 2:
                    matriz_Ke_final[0, 1] = (3 * evalor * ivalor) / largura_elem[0]
                    matriz_Ke_final[0, 2] = (4 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[0, 3] = (2 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 2] = (2 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 3] = (4 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 4] = (3 * evalor * ivalor) / largura_elem[2]
                else:
                    # definindo as variáveis auxiliares
                    num_colunas = len(momentos_2)
                    anteantepnultima = num_colunas - 4
                    antepenultima = num_colunas - 3
                    penultima = num_colunas - 2
                    for i in range(num_D_matriz):
                        for j in range(num_colunas-1):
                            if i == 0: # primeira linha
                                if j == i+1:
                                    matriz_Ke_final[i,j] = (3*evalor*ivalor)/largura_elem[i]
                                elif j == i+2:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i+1]
                                elif j == i+3:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i+1]
                            elif i < num_D_matriz-1: # segunda até penúltima linha
                                if j == i+1:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i]
                                elif j == i+2:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i]
                                elif j == i+3:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i+1]
                                elif j == i+4:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i+1]
                            else: # última linha
                                if j == anteantepnultima:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i]
                                elif j == antepenultima:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i]
                                elif j == penultima:
                                    matriz_Ke_final[i,j] = (3*evalor*ivalor)/largura_elem[i+1]

                mult_D_K = matriz_Ke_final*D_matriz_correta
                global soma_D_K
                global momento_negativo_geral
                soma_D_K = np.sum(mult_D_K, axis=0)
                momento_negativo_final = momentos_2 + soma_D_K
                momento_negativo_geral = list(filter(lambda x: x < 0, momento_negativo_final))
                global forca_barra
                forca_barra = []
                
                forca_barra1dir = 3 * forca_elem[0] * largura_elem[0]/8
                forca_barra.append(forca_barra1dir)
                forca_1 = (5 * forca_elem[0] * largura_elem[0]) / 8
                forca_barra.append(forca_1)
                for i in range(1, len(forca_elem)-1):
                    q = forca_elem[i]
                    l = largura_elem[i]
                    forca_2 = (q * l) / 2
                    forca_barra.append(forca_2)
                    forca_barra.append(forca_2)
                forca_penultima_esq = (5 * forca_elem[-1] * largura_elem[-1]) / 8
                forca_barra.append(forca_penultima_esq)
                forca_ultima_barraesq = 3 * forca_elem[-1] * largura_elem[-1]/8
                forca_barra.append(forca_ultima_barraesq)
                num_colunas = len(momentos_2)
                anteantepnultima = num_colunas - 4
                antepenultima = num_colunas - 3
                penultima = num_colunas - 2
                ultima = penultima + 1 
                global matriz_Ke_reacoes
                if valor_entry == 3:
                    matriz_Ke_reacoes = np.zeros((num_D_matriz, len(momentos_2)))
                else:
                    matriz_Ke_reacoes = np.zeros((num_D_matriz, len(momentos_2)))
                for i in range(num_D_matriz):
                    for j in range(num_colunas):
                        if i == 0: # primeira linha
                            if j == i:
                                matriz_Ke_reacoes[i,j] = (3*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == i+1:
                                matriz_Ke_reacoes[i,j] = (-3*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == i+2:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == i+3:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i+1]**2)
                        elif i < num_D_matriz-1: # segunda até penúltima linha
                            if j == i+2:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == i+3:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i+1]**2)
                        else: # última linha
                            if j == anteantepnultima:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == antepenultima:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == penultima:
                                matriz_Ke_reacoes[i,j] = (3*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == ultima:
                                matriz_Ke_reacoes[i,j] = (-3*evalor*ivalor)/(largura_elem[i+1]**2)
                global mult_D_K_reacoes
                mult_D_K_reacoes = matriz_Ke_reacoes * D_matriz_correta
                global soma_D_K_reacoes
                global reacoes_final
                global soma_lista_meio
                soma_D_K_reacoes = np.sum(mult_D_K_reacoes, axis=0)
                reacoes_final = forca_barra + soma_D_K_reacoes
                soma_lista_meio = [reacoes_final[i] + reacoes_final[i+1] for i in range(1, len(reacoes_final)-1, 2)]
                reacoes_final_1 = reacoes_final[0]
                reacoes_final_ultimo = reacoes_final[-1]
                soma_lista_meio.insert(0, reacoes_final_1)
                soma_lista_meio.append(reacoes_final_ultimo)
                global termo_dist_1
                global momentos_positivosf
                momentos_positivosf = []
                termo_dist_1 = []
                va_atual = soma_lista_meio[0]
                for i in range(len(soma_lista_meio)):
                    termo_dist_1.append(va_atual)
                    if i < len(soma_lista_meio) - 1:
                        va_atual = va_atual - forca_elem[i]*largura_elem[i] + soma_lista_meio[i+1]
                termo_dist_1.pop()
                for i in range(len(termo_dist_1)):
                    dist_x = termo_dist_1[i]*largura_elem[i]/(forca_elem[i]*largura_elem[i])
                    dist_x_reacoes.append(dist_x)
                momentos_positivos = (termo_dist_1[0] * dist_x_reacoes[0])/2
                for i in range(len(termo_dist_1)):
                    momentos_positivosf.append(momentos_positivos)
                    if i < len(termo_dist_1) - 1:
                        momentos_positivos = ((termo_dist_1[i+1] * dist_x_reacoes[i+1])/2) + momento_negativo_geral[i]
                momentos_unidos_final = list(chain(*zip_longest(momentos_positivosf, momento_negativo_geral)))
        if valor_entry == 3 and passeiocombod.get() == "não" and passeiocomboe.get() == "não":
            momento_barra1dir = -forca_elem[0] * largura_elem[0]**2/8
            momentos.append(momento_barra1dir)
            Ke_simples = (3 * evalor * ivalor)/largura_elem[0]
            Ke_.append(Ke_simples)
            for i in range(1, len(forca_elem) - 1):
                q = forca_elem[i]
                l = largura_elem[i]
                momento = (q * l ** 2) / 12
                Ke = evalor * ivalor * 4 / l
                Ke_.append(Ke)
                Ke_.append(Ke)
                if i % 2 == 0:
                    momentos.append(-momento)
                    momentos.append(momento)
                else:
                    momentos.append(momento)
                    momentos.append(-momento)
            momento_ultima_barraesq = forca_elem[-1] * (largura_elem[-1]**2)/8
            momentos.append(momento_ultima_barraesq)
            Ke_ultimo = (3 * evalor * ivalor)/largura_elem[-1]
            Ke_.append(Ke_ultimo)
            for i in range(0, len(momentos), 2):
                soma = momentos[i] + momentos[i+1]
                beta.append(soma)
                soma_ke = Ke_[i] + Ke_[i+1]
                Ke_soma.append(soma_ke)
                Ke_matriz = np.diag(Ke_soma)
                Ke_auxiliar = [Ke_[i] for i in range(1,len(Ke_))]
                for i in range(len(Ke_matriz)):
                    for j in range(len(Ke_matriz)):
                        if i == j:
                            continue  # pula a diagonal principal
                        elif abs(i - j) == 1:
                            Ke_matriz[i][j] = Ke_auxiliar[i] / 2  # atualiza elementos com diferença i-j = 1 
                        else:
                            Ke_matriz[i][j] = 0  # zera os demais elementos
                beta2 = np.array([-1 * b for b in beta])
                beta_matriz = np.array([beta2])
                D_matriz_correta = np.linalg.solve(Ke_matriz, beta_matriz.T)
                D_matriz = D_matriz_correta.T
                momentos_2 = momentos.copy()  # copia a lista original
                momentos_2.insert(0, 0)  # adiciona 0 no índice 0
                momentos_2.append(0)  # adiciona 0 no final da lista
                num_D_matriz = D_matriz.shape[1]
                if valor_entry == 3:
                    matriz_Ke_final = np.zeros((num_D_matriz, len(momentos_2)))
                else:
                    matriz_Ke_final = np.zeros((num_D_matriz, len(momentos_2)))  
                if num_D_matriz == 2:
                    matriz_Ke_final[0, 1] = (3 * evalor * ivalor) / largura_elem[0]
                    matriz_Ke_final[0, 2] = (4 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[0, 3] = (2 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 2] = (2 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 3] = (4 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 4] = (3 * evalor * ivalor) / largura_elem[2]
                else:
                    # definindo as variáveis auxiliares
                    num_colunas = len(momentos_2)
                    anteantepnultima = num_colunas - 4
                    antepenultima = num_colunas - 3
                    penultima = num_colunas - 2
                    for i in range(num_D_matriz):
                        for j in range(num_colunas-1):
                            if i == 0: # primeira linha
                                if j == i+1:
                                    matriz_Ke_final[i,j] = (3*evalor*ivalor)/largura_elem[i]
                                elif j == i+2:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i+1]
                                elif j == i+3:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i+1]
                            elif i < num_D_matriz-1: # segunda até penúltima linha
                                if j == i+1:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i]
                                elif j == i+2:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i]
                                elif j == i+3:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i+1]
                                elif j == i+4:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i+1]
                            else: # última linha
                                if j == anteantepnultima:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i]
                                elif j == antepenultima:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i]
                                elif j == penultima:
                                    matriz_Ke_final[i,j] = (3*evalor*ivalor)/largura_elem[i+1]

                mult_D_K = matriz_Ke_final*D_matriz_correta
                soma_D_K = np.sum(mult_D_K, axis=0)
                momento_negativo_final = momentos_2 + soma_D_K
                momento_negativo_geral = list(filter(lambda x: x < 0, momento_negativo_final))
                forca_barra = []
                
                forca_barra1dir = 3 * forca_elem[0] * largura_elem[0]/8
                forca_barra.append(forca_barra1dir)
                forca_1 = (5 * forca_elem[0] * largura_elem[0]) / 8
                forca_barra.append(forca_1)
                for i in range(1, len(forca_elem)-1):
                    q = forca_elem[i]
                    l = largura_elem[i]
                    forca_2 = (q * l) / 2
                    forca_barra.append(forca_2)
                    forca_barra.append(forca_2)
                forca_penultima_esq = (5 * forca_elem[-1] * largura_elem[-1]) / 8
                forca_barra.append(forca_penultima_esq)
                forca_ultima_barraesq = 3 * forca_elem[-1] * largura_elem[-1]/8
                forca_barra.append(forca_ultima_barraesq)
                num_colunas = len(momentos_2)
                anteantepnultima = num_colunas - 4
                antepenultima = num_colunas - 3
                penultima = num_colunas - 2
                ultima = penultima + 1 
                if valor_entry == 3:
                    matriz_Ke_reacoes = np.zeros((num_D_matriz, len(momentos_2)))
                else:
                    matriz_Ke_reacoes = np.zeros((num_D_matriz, len(momentos_2)))
                for i in range(num_D_matriz):
                    for j in range(num_colunas):
                        if i == 0: # primeira linha
                            if j == i:
                                matriz_Ke_reacoes[i,j] = (3*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == i+1:
                                matriz_Ke_reacoes[i,j] = (-3*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == i+2:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == i+3:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i+1]**2)
                        elif i < num_D_matriz-1: # segunda até penúltima linha
                            if j == i+2:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == i+3:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i+1]**2)
                        else: # última linha
                            if j == anteantepnultima:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == antepenultima:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == penultima:
                                matriz_Ke_reacoes[i,j] = (3*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == ultima:
                                matriz_Ke_reacoes[i,j] = (-3*evalor*ivalor)/(largura_elem[i+1]**2)
                mult_D_K_reacoes = matriz_Ke_reacoes * D_matriz_correta
                soma_D_K_reacoes = np.sum(mult_D_K_reacoes, axis=0)
                reacoes_final = forca_barra + soma_D_K_reacoes
                soma_lista_meio = [reacoes_final[i] + reacoes_final[i+1] for i in range(1, len(reacoes_final)-1, 2)]
                reacoes_final_1 = reacoes_final[0]
                reacoes_final_ultimo = reacoes_final[-1]
                soma_lista_meio.insert(0, reacoes_final_1)
                soma_lista_meio.append(reacoes_final_ultimo)
                momentos_positivosf = []
                termo_dist_1 = []
                va_atual = soma_lista_meio[0]
                for i in range(len(soma_lista_meio)):
                    termo_dist_1.append(va_atual)
                    if i < len(soma_lista_meio) - 1:
                        va_atual = va_atual - forca_elem[i]*largura_elem[i] + soma_lista_meio[i+1]
                termo_dist_1.pop()
                for i in range(len(termo_dist_1)):
                    dist_x = termo_dist_1[i]*largura_elem[i]/(forca_elem[i]*largura_elem[i])
                    dist_x_reacoes.append(dist_x)
                momentos_positivos = (termo_dist_1[0] * dist_x_reacoes[0])/2
                for i in range(len(termo_dist_1)):
                    momentos_positivosf.append(momentos_positivos)
                    if i < len(termo_dist_1) - 1:
                        momentos_positivos = ((termo_dist_1[i+1] * dist_x_reacoes[i+1])/2) + momento_negativo_geral[i]
                momentos_unidos_final = list(chain(*zip_longest(momentos_positivosf, momento_negativo_geral)))
        elif valor_entry > 3 and passeiocombod.get() == "não" and passeiocomboe.get() == "não":
            momento_barra1dir = -forca_elem[0] * largura_elem[0]**2/8
            momentos.append(momento_barra1dir)
            Ke_simples = (3 * evalor * ivalor)/largura_elem[0]
            Ke_.append(Ke_simples)
            for i in range(1, len(forca_elem)-1):
                q = forca_elem[i]
                l = largura_elem[i]
                momento = (q * l ** 2) / 12
                Ke = evalor * ivalor * 4 / l
                Ke_.append(Ke)
                Ke_.append(Ke)
                if i % 2 == 0:
                    momentos.append(momento)
                    momentos.append(-momento)
                else:
                    momentos.append(momento)
                    momentos.append(-momento)
            momento_ultima_barraesq = forca_elem[-1] * (largura_elem[-1]**2)/8
            momentos.append(momento_ultima_barraesq)
            Ke_ultimo = (3 * evalor * ivalor)/largura_elem[-1]
            Ke_.append(Ke_ultimo)
            for i in range(0, len(momentos), 2):
                soma = momentos[i] + momentos[i+1]
                beta.append(soma)
                soma_ke = Ke_[i] + Ke_[i+1]
                Ke_soma.append(soma_ke)
                Ke_matriz = np.diag(Ke_soma)
                Ke_auxiliar = [Ke_[i] for i in range(1,len(Ke_))]
                for i in range(len(Ke_matriz)):
                    for j in range(len(Ke_matriz)):
                        if i == j:
                            continue  # pula a diagonal principal
                        elif abs(i - j) == 1:
                            Ke_matriz[i][j] = Ke_auxiliar[i] / 2  # atualiza elementos com diferença i-j = 1 
                        else:
                            Ke_matriz[i][j] = 0  # zera os demais elementos
                beta2 = np.array([-1 * b for b in beta])
                beta_matriz = np.array([beta2])
                D_matriz_correta = np.linalg.solve(Ke_matriz, beta_matriz.T)
                D_matriz = D_matriz_correta.T
                momentos_2 = momentos.copy()  # copia a lista original
                momentos_2.insert(0, 0)  # adiciona 0 no índice 0
                momentos_2.append(0)  # adiciona 0 no final da lista
                num_D_matriz = D_matriz.shape[1]
                if valor_entry == 3:
                    matriz_Ke_final = np.zeros((num_D_matriz, len(momentos_2)))
                else:
                    matriz_Ke_final = np.zeros((num_D_matriz, len(momentos_2)))  
                if num_D_matriz == 2:
                    matriz_Ke_final[0, 1] = (3 * evalor * ivalor) / largura_elem[0]
                    matriz_Ke_final[0, 2] = (4 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[0, 3] = (2 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 2] = (2 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 3] = (4 * evalor * ivalor) / largura_elem[1]
                    matriz_Ke_final[1, 4] = (3 * evalor * ivalor) / largura_elem[2]
                else:
                    # definindo as variáveis auxiliares
                    num_colunas = len(momentos_2)
                    anteantepnultima = num_colunas - 4
                    antepenultima = num_colunas - 3
                    penultima = num_colunas - 2
                    for i in range(num_D_matriz):
                        for j in range(num_colunas-1):
                            if i == 0: # primeira linha
                                if j == i+1:
                                    matriz_Ke_final[i,j] = (3*evalor*ivalor)/largura_elem[i]
                                elif j == i+2:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i+1]
                                elif j == i+3:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i+1]
                            elif i < num_D_matriz-1: # segunda até penúltima linha
                                if j == i+1:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i]
                                elif j == i+2:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i]
                                elif j == i+3:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i+1]
                                elif j == i+4:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i+1]
                            else: # última linha
                                if j == anteantepnultima:
                                    matriz_Ke_final[i,j] = (2*evalor*ivalor)/largura_elem[i]
                                elif j == antepenultima:
                                    matriz_Ke_final[i,j] = (4*evalor*ivalor)/largura_elem[i]
                                elif j == penultima:
                                    matriz_Ke_final[i,j] = (3*evalor*ivalor)/largura_elem[i+1]

                mult_D_K = matriz_Ke_final*D_matriz_correta
                soma_D_K = np.sum(mult_D_K, axis=0)
                momento_negativo_final = momentos_2 + soma_D_K
                momento_negativo_geral = list(filter(lambda x: x < 0, momento_negativo_final))
                forca_barra = []
                
                forca_barra1dir = 3 * forca_elem[0] * largura_elem[0]/8
                forca_barra.append(forca_barra1dir)
                forca_1 = (5 * forca_elem[0] * largura_elem[0]) / 8
                forca_barra.append(forca_1)
                for i in range(1, len(forca_elem)-1):
                    q = forca_elem[i]
                    l = largura_elem[i]
                    forca_2 = (q * l) / 2
                    forca_barra.append(forca_2)
                    forca_barra.append(forca_2)
                forca_penultima_esq = (5 * forca_elem[-1] * largura_elem[-1]) / 8
                forca_barra.append(forca_penultima_esq)
                forca_ultima_barraesq = 3 * forca_elem[-1] * largura_elem[-1]/8
                forca_barra.append(forca_ultima_barraesq)
                num_colunas = len(momentos_2)
                anteantepnultima = num_colunas - 4
                antepenultima = num_colunas - 3
                penultima = num_colunas - 2
                ultima = penultima + 1 
                if valor_entry == 3:
                    matriz_Ke_reacoes = np.zeros((num_D_matriz, len(momentos_2)))
                else:
                    matriz_Ke_reacoes = np.zeros((num_D_matriz, len(momentos_2)))
                for i in range(num_D_matriz):
                    for j in range(num_colunas):
                        if i == 0: # primeira linha
                            if j == i:
                                matriz_Ke_reacoes[i,j] = (3*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == i+1:
                                matriz_Ke_reacoes[i,j] = (-3*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == i+2:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == i+3:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i+1]**2)
                        elif i < num_D_matriz-1: # segunda até penúltima linha
                            if j == i+2:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == i+3:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i+1]**2)
                        else: # última linha
                            if j == anteantepnultima:
                                matriz_Ke_reacoes[i,j] = (6*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == antepenultima:
                                matriz_Ke_reacoes[i,j] = (-6*evalor*ivalor)/(largura_elem[i]**2)
                            elif j == penultima:
                                matriz_Ke_reacoes[i,j] = (3*evalor*ivalor)/(largura_elem[i+1]**2)
                            elif j == ultima:
                                matriz_Ke_reacoes[i,j] = (-3*evalor*ivalor)/(largura_elem[i+1]**2)
                mult_D_K_reacoes = matriz_Ke_reacoes * D_matriz_correta
                soma_D_K_reacoes = np.sum(mult_D_K_reacoes, axis=0)
                reacoes_final = forca_barra + soma_D_K_reacoes
                soma_lista_meio = [reacoes_final[i] + reacoes_final[i+1] for i in range(1, len(reacoes_final)-1, 2)]
                reacoes_final_1 = reacoes_final[0]
                reacoes_final_ultimo = reacoes_final[-1]
                soma_lista_meio.insert(0, reacoes_final_1)
                soma_lista_meio.append(reacoes_final_ultimo)
                momentos_positivosf = []
                termo_dist_1 = []
                va_atual = soma_lista_meio[0]
                for i in range(len(soma_lista_meio)):
                    termo_dist_1.append(va_atual)
                    if i < len(soma_lista_meio) - 1:
                        va_atual = va_atual - forca_elem[i]*largura_elem[i] + soma_lista_meio[i+1]
                termo_dist_1.pop()
                for i in range(len(termo_dist_1)):
                    dist_x = termo_dist_1[i]*largura_elem[i]/(forca_elem[i]*largura_elem[i])
                    dist_x_reacoes.append(dist_x)
                momentos_positivos = (termo_dist_1[0] * dist_x_reacoes[0])/2
                for i in range(len(termo_dist_1)):
                    momentos_positivosf.append(momentos_positivos)
                    if i < len(termo_dist_1) - 1:
                        momentos_positivos = ((termo_dist_1[i+1] * dist_x_reacoes[i+1])/2) + momento_negativo_geral[i]
                momentos_unidos_final = list(chain(*zip_longest(momentos_positivosf, momento_negativo_geral)))  


            
            
    
    def mostrar_valores():
        def desenhar_grafico_positivo():
            # Lógica para desenhar o gráfico positivo
            x = np.linspace(-10, 10, 100)
            y = x**2
            fig = Figure(figsize=(2, 1), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            ax.plot(x, y)
            ax.axis('off')
            canvas = FigureCanvasTkAgg(fig, master=page1)
            canvas.draw()
            canvas.get_tk_widget().grid(row=14, column=1, pady= 10)
        
        def desenhar_grafico_negativo():
            # Lógica para desenhar o gráfico negativo
            # Gerando os valores de x
            x = np.linspace(-10, 10, 100)

            # Definindo uma função exponencial para o triângulo
            def exponential_triangle(x):
                return np.exp(-np.abs(x))

            # Calculando os valores correspondentes de y
            y = exponential_triangle(x)
            fig = Figure(figsize=(2, 1), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            ax.plot(x, y)
            ax.axis('off')
            canvas = FigureCanvasTkAgg(fig, master=page1)
            canvas.draw()
            canvas.get_tk_widget().grid(row=14, column=1, pady= 10)
        
        def selecionar_opcao(event):
            valor_selecionado = float(combobox_momentos.get())
            indice_selecionado = momentos_unidos_final.index(valor_selecionado)
            label_valor_momentos.config(text="Momento:")
            text_valor_momentos.delete(1.0, tk.END)
            text_valor_momentos.insert(tk.END, valor_selecionado)
            if valor_selecionado >= 0:
                desenhar_grafico_positivo()
            else:
                desenhar_grafico_negativo()



        def criar_combobox(lista_opcoes):
            global text_comprimento
            global label_comprimento
            global text_valor_momentos
            global label_valor_momentos
            global combobox_momentos
            combobox_momentos = ttk.Combobox(page1, values=lista_opcoes)
            combobox_momentos.current(0)  # Define o primeiro valor como selecionado
            combobox_momentos.grid(row=12, column=2, pady= 10)
            combobox_momentos.bind("<<ComboboxSelected>>", selecionar_opcao)
            label_valor_momentos = ttk.Label(page1, text="Momentos:")
            label_valor_momentos.grid(row=13, column=0, pady= 10)

            text_valor_momentos = tk.Text(page1, height=1, width=10)
            text_valor_momentos.grid(row=13, column=1, pady= 10)

        criar_combobox(momentos_unidos_final)
        
        # Criar o conteúdo do bloco de notas
        momentos_2_notas = f"Os momentos são: {momentos_2}"
        beta_matriz_notas = f"Os valores de beta são: {beta_matriz}"
        Ke_notas = f"Os Ke,s são: {Ke_}"
        Ke_Matriz_notas = f"A matriz Ke é: {Ke_matriz}"
        D_matriz_notas = f"As deslocabilidades são: {D_matriz}"
        matriz_Ke_notas = f"Os Ke,s globais são: {matriz_Ke_final}"
        reacoes_notas = f"As reações são: {soma_lista_meio}"
        momentos_negativos_notas = f"Os momentos negativos são: {momento_negativo_geral}"
        momentos_positivos_notas = f"Os momentos positivos são: {momentos_positivosf}"

    
        # Criar o arquivo de bloco de notas
        with open("bloco_notas.txt", "w") as arquivo:
            arquivo.write(momentos_2_notas + "\n")
            arquivo.write(beta_matriz_notas + "\n")
            arquivo.write(Ke_notas + "\n")
            arquivo.write(Ke_Matriz_notas + "\n")
            arquivo.write(D_matriz_notas + "\n")
            arquivo.write(matriz_Ke_notas + "\n")
            arquivo.write(reacoes_notas + "\n")
            arquivo.write(momentos_negativos_notas + "\n")
            arquivo.write(momentos_positivos_notas + "\n")
        
        
        
        



    botao = ttk.Button(page1, text='calcular', command=Valor_momento_1_elemento)
    botao.grid(row=12, column=0, pady= 10)

    botao = ttk.Button(page1, text='Mostrar valores', command=mostrar_valores)
    botao.grid(row=12, column=1, pady= 10)

    



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

