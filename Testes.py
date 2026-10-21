import tkinter as tk
import pyperclip

def atualizar_texto():
    # Obter o valor float do widget de texto na página 1
    valor_float = float(page1_text.get())

    # Atualizar o widget de texto na página 2
    page2_text.delete(1.0, tk.END)
    page2_text.insert(tk.END, str(valor_float))

    # Copiar o valor para a área de transferência
    pyperclip.copy(str(valor_float))

# Criar a janela principal
root = tk.Tk()

# Criar a página 1
page1_frame = tk.Frame(root)
page1_frame.pack()

page1_label = tk.Label(page1_frame, text="Valor na página 1:")
page1_label.pack()

page1_text = tk.Entry(page1_frame)
page1_text.pack()

# Criar a página 2
page2_frame = tk.Frame(root)
page2_frame.pack()

page2_label = tk.Label(page2_frame, text="Valor na página 2:")
page2_label.pack()

page2_text = tk.Entry(page2_frame)
page2_text.pack()

# Botão para atualizar o valor na página 2
atualizar_button = tk.Button(root, text="Atualizar", command=atualizar_texto)
atualizar_button.pack()

# Iniciar a aplicação
root.mainloop()