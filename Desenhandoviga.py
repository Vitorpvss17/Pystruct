from tkinter import *

root = Tk()

canvas = Canvas(root, width=600, height=300)
canvas.pack()

# Desenhando a viga
beam = canvas.create_line(50, 250, 550, 250, fill="black", width=3)

# Desenhando os apoios
triangle1 = canvas.create_line(50, 250, 60, 260, fill="black", width=3)
triangle1 = canvas.create_line(50, 250, 40, 260, fill="black", width=3)
triangle1 = canvas.create_line(60, 260, 40, 260, fill="black", width=3)

triangle2 = canvas.create_line(550, 250, 560, 260, fill="black", width=3)
triangle2 = canvas.create_line(550, 250, 540, 260, fill="black", width=3)
triangle2 = canvas.create_line(560, 260, 540, 260, fill="black", width=3)

# Desenhando as cargas concentradas
rectangle1 = canvas.create_line(50, 250, 50, 210, fill="black", width=3)
rectangle1 = canvas.create_line(50, 210, 550, 210, fill="black", width=3)
rectangle1 = canvas.create_line(550, 210, 550, 250, fill="black", width=3)
root.mainloop()

