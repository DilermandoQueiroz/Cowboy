from algebrageo import *
from math import *
import matplotlib.pyplot as plt
from numpy import *
import time
import teste

def mostrar(x):
    for c in range(0, len(x)):
        print(x[c],'atomo numero', c)

def angulo(x):
    angulos=list()
    a = list()
    for n in range(2, len(x)-1):
        for c in range(0, len(x[n])):
            a.append(x[n][c] - x[n-1][c])

        b = list()
        for c in range(0, len(x[n])):
            b.append(x[n][c] - x[n+1][c])

        aux = 0
        aux2 = 0
        aux3 = 0
        for c in range(0, 3):
            aux = aux + a[c]*b[c]
            aux2 = aux2 + a[c]**2
            aux3 = aux3 + b[c]**2
            resultado = acos(aux / (sqrt(aux2) * sqrt(aux3)))
        angulos.append(resultado)
        a.clear()
        b.clear()

    return angulos

def distancia(x):
    di = list()
    aux1 = list()
    aux = 0
    for n in range(0, len(x)):
        for l in range(0, len(x)):
            if(l!=n):
                for c in range(0, 3):
                    aux = aux + (x[l][c]-x[n][c])**2
            else:
                aux = 0
            aux = sqrt(aux)
            aux1.append(aux)
            aux = 0
        di.append(aux1[:])
        aux1.clear()

    return di

def tresatomos(x):
    multr = list()
    aux = list()
    for l in range(0, 3):
        for c in range(0, 3):
            adicionar(x[l][c], 2**c, aux)
        multr.append(aux[:])
        aux.clear()
    return multr

def ExibirMolecula(atomo):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = list()
    y = list()
    z = list()

    for c in range(0, len(atomo)):
            for k in range(0, 3):
                if(atomo[c][k][1] == 1):
                    x.append(atomo[c][k][0])
                if (atomo[c][k][1] == 2):
                    y.append(atomo[c][k][0])
                if (atomo[c][k][1] == 4):
                    z.append(atomo[c][k][0])

    X = [-30.003, -30.733, -31.987, -32.256, -31.873, -32.876]
    Y = [7.946, 6.951, 6.879, 8.14, 5.666, 5.637]
    Z = [35.233, 35.323, 34.568, 33.83, 33.608, 32.655]

    ax.scatter(x,y,z, c='r', marker='o')
    ax.scatter(x, y, z, c='g', marker='o')
    plt.show()

def Pai(i):
    if(i%2 != 0):
        pai = (i+1)/2
    else:
        pai = i/2

    pai = int(pai)
    return pai

def Avo(i):
    avo = Pai(Pai(i))
    avo = int(avo)
    return avo

def NivelAtomo(i):
    c=0
    while(c>=0):
        if(2**c < i <= 2**(c+1)):
            nivel = c + 2
            return nivel
        c+=1

def raio(x):
    global r
    for c in range(0, len(x)):
        if(c==0):
            r.append([[0,0]])
        elif(c==1 or c==2):
            r.append(sub(x[c], x[c - 1]))
        else:
            r.append(sub(x[c], x[Pai(c)]))
    return r

def rteta(r, di, i):
    h = NivelAtomo(i)
    aux = [[-di[h][h - 1] / di[h - 1][h - 2], 0]]
    rit = pgeometrico(aux, r[Pai(i)])
    return rit

def RTeta(r, teta, i):
    B = pexterno(r[Pai(i)],r[Avo(i)])
    B = norma(B)
    R = rotor(B, teta)
    return R

def omega(di, i):
    i = NivelAtomo(i)
    d123 = (di[i-3][i-2]**2) + (di[i-2][i-1]**2) - (di[i-3][i-1]**2)
    d012 = (di[i-2][i-1]**2) + (di[i-2][i]**2) - (di[i-1][i]**2)
    s = 2 * (di[i-2][i-1]**2) * ((di[i-3][i-2]**2) + (di[i-2][i]**2) - (di[i-3][i]**2)) - (d123 * d012)
    l = sqrt(4 * (di[i-3][i-2]**2) * (di[i-2][i-1]**2) - (d123**2)) * sqrt(4 * (di[i-2][i-1]**2) * (di[i-2][i]**2) - (d012**2))
    w = s/l
    w = acos(w)
    return w

def romega(rteta, RTeta):
    romega = pgeometrico(RTeta, rteta)
    romega2 = pgeometrico(romega, reverso(RTeta, -1))
    return romega2

def Romega(r, omega, i):
    Bomega = contracaoesq(r[Pai(i)], [[1,7]])
    Bomega = norma(Bomega)
    if (i % 2 != 0):
        omega = omega + pi
    else:
        omega = -omega + pi

    Romega = rotor(Bomega, omega)

    return Romega

def ri(Romega, romega):
    multr = pgeometrico(Romega, romega)
    multr = pgeometrico(multr, reverso(Romega, -1))
    return multr

'''
Retirar o blade e1e2e3 do raio, ele atrapalhava as contas
'''

def conferir(mult):
    for c in range(0, len(mult)):
        if(c==3):
            del(mult[3])

    return mult

def iniciar(x, r, di, teta, qtde):
    for i in range(3, qtde):
        rt = rteta(r, di, i)
        t = teta[NivelAtomo(i)-3]
        Rt = RTeta(r, t, i)
        rw = romega(rt, Rt)
        w = omega(di, i)
        Rw = Romega(r, w, i)
        raio = ri(Rw, rw)
        raio = conferir(raio)                
        r.append(raio)
        xi = soma(x[Pai(i)], r[i])
        #xi = conferir(xi)
        x.append(xi)
    return x

if __name__ == "__main__":
    inicio = time.time()

    #atomo correto
    m0k = [[-30.003, 7.946, 35.233],
           [-30.733, 6.951, 35.323],
           [-31.987, 6.879, 34.568],
           [-32.256, 8.140, 33.830],
           [-31.873, 5.666, 33.608],
           [-32.876, 5.637, 32.655]]

    xcorreto = teste.feb

    # 3 atomos de entrada
    x = tresatomos(xcorreto)

    #angulo entre os atomos
    teta = angulo(xcorreto)

    #matriz das distancias entre os atomos obtida pela RMN
    di = distancia(xcorreto)

    #tamanho da molecula
    tam = len(xcorreto)
    qtde = 2**(tam-2)+1

    #raio
    r = list()
    raio(x)

    xc = iniciar(x, r, di, teta, qtde)
    mostrar(xc)
    #ExibirMolecula(x)
    #latex(xc)

    fim = time.time()

    print(fim - inicio)