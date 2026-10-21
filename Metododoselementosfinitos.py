import sympy as sp
import math as mt
sp.init_printing()

#simbolos utilizados
I, E, A, L, theta = sp.symbols(['I', 'E', 'A', 'L', 'theta'])
c = sp.cos(theta)
s = sp.sin(theta)
#Esforços
symbols_force = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']
symbols_disp = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9']
s1, s2, s3, s4, s5, s6, s7, s8, s9 = sp.symbols(symbols_force)
q1, q2, q3, q4, q5, q6, q7, q8, q9 = sp.symbols(symbols_disp)
#Matriz de rigidez local do elemento
ke_ = sp.Matrix([
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


#Função para criar o elemento de viga com rigidez axial


def beam(I_, E_, A_, L_, theta_, g1, g2, g3, g4, g5, g6):
    theta_ = theta_ * mt.pi / 180.
    K_element = Ke.subs([
        (I, I_),
        (E, E_),
        (A, A_),
        (L, L_),
        (theta, theta_)
    ])
    K_element = K_element.row_insert(0, sp.Matrix([[g1, g2, g3, g4, g5, g6]]))
    K_element = K_element.col_insert(0, sp.Matrix([0, g1, g2, g3, g4, g5, g6]))

    return K_element


beam1 = beam(1, 1, 1, 1, 0, 1, 2, 3, 4, 5, 6)
beam2 = beam(1, 1, 1, 1, 0, 4, 5, 6, 7, 8, 9)
print(beam1)
print(beam2)

#Armazena as matrizes de rigidez de todos os elementos (usar metodo append)
k_elementos = []

k_elementos.append(beam1)
k_elementos.append(beam2)

n_de_elementos = len(k_elementos)
n_de_GDL = 9
K_struct = sp.Matrix.zeros(n_de_GDL, n_de_GDL)
for n in range(n_de_elementos):
    GDL = []
    GDL.append(k_elementos[n][0, 1] - 1)
    GDL.append(k_elementos[n][0, 2] - 1)
    GDL.append(k_elementos[n][0, 3] - 1)
    GDL.append(k_elementos[n][0, 4] - 1)
    GDL.append(k_elementos[n][0, 5] - 1)
    GDL.append(k_elementos[n][0, 6] - 1)

    for i in range(len(GDL)):
        for j in range(len(GDL)):
            K_struct[GDL[i], GDL[j]] += k_elementos[n][i+1, j+1]


print(K_struct)
F = sp.Matrix([s1, s2, 0, 0, -100e3, 0, s7, s8, 0])
u = sp.Matrix([0, 0, q3, q4, q5, q6, 0, 0, q9])
#Resolução do sistema linear

system = K_struct * u - F
resultado = sp.linsolve(system,(s1, s2, q3, q4, q5, q6, s7, s8, q9))
print(resultado)