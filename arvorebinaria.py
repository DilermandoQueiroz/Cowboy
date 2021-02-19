from algebrageo import *
from math import *
import protein

'''
Arvore de busca para o PGDMD com distancias exatas
'''

class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None
        self.pai = None
        self.calc = None

    def __str__(self):
        return str(self.data)


class BinaryTree:
    def __init__(self, data=None, node=None):
        if node:
            self.root = node
        elif data:
            node = Node(data)
            self.root = node
        else:
            self.root = None

    def exibir(self, node=None):
        if node is None:
            node = self.root
        if node.left:
            print(node.data)
            self.exibir(node.left)
        if node.right:
            print(node.data)
            self.exibir(node.right)

    def insertion(self, no, i):
        global n
        if (i <= n - 1):            # n é a quantidade de atomos
            x = calcular(no, i, 0)  # 0 para calcular posição a esquerda
            x2 = calcular(no, i, 1)  # 1 para calcular posição a direita

            if validade(no, x, i) == True:
                e = Node(x)
                no.left = e
                e.pai = no
                self.insertion(e, i+1)
            else:
                no.left = None

            if validade(no, x2, i) == True and i > 3:
                d = Node(x2)
                no.right = d
                d.pai = no
                self.insertion(d, i+1)
            else:
                no.right = None

            if no.right == None and no.left == None:
                no.data = None


def calcular(no, i, ramo):
    global teta, di

    rTeta = pgeometrico([[-1 * (di[i][i - 1]) / di[i - 1][i - 2], 0]],
                        sub(no.data, no.pai.data))

    RotorTeta = rotor(norma(pexterno(sub(no.data, no.pai.data),
                                     sub(no.pai.data, no.pai.pai.data))), teta[i-3])

    rOmega = pgeometrico(pgeometrico(RotorTeta, rTeta), reverso(RotorTeta, -1))

    if(ramo == 0):
        RotorOmega = rotor(norma(contracaoesq(sub(no.data, no.pai.data), [[1, 7]])),
                           omega(i) + math.pi)

        r = pgeometrico(pgeometrico(RotorOmega, rOmega),
                        reverso(RotorOmega, -1))

        r = conferir(r)

        return soma(no.data, r)

    else:
        RotorOmega2 = rotor(norma(contracaoesq(sub(no.data, no.pai.data), [[1, 7]])),
                            -1*omega(i) + math.pi)

        r2 = pgeometrico(pgeometrico(RotorOmega2, rOmega),
                         reverso(RotorOmega2, -1))

        r2 = conferir(r2)

        return soma(no.data, r2)


def conferir(mult):
    for c in range(0, len(mult)):
        if(c == 3):
            del(mult[3])

    return mult


def omega(i):
    global di
    d123 = (di[i-3][i-2]**2) + (di[i-2][i-1]**2) - (di[i-3][i-1]**2)
    d012 = (di[i-2][i-1]**2) + (di[i-2][i]**2) - (di[i-1][i]**2)
    s = 2 * (di[i-2][i-1]**2) * ((di[i-3][i-2]**2) +
                                 (di[i-2][i]**2) - (di[i-3][i]**2)) - (d123 * d012)
    l = math.sqrt(4 * (di[i-3][i-2]**2) * (di[i-2][i-1]**2) - (d123**2)) * \
        math.sqrt(4 * (di[i-2][i-1]**2) * (di[i-2][i]**2) - (d012**2))
    w = s/l
    w = math.acos(w)
    return w


def validade(no, x, i):
    global di

    aux = 0

    if i > 3:
        for c in range(0, len(x)):
            aux = aux + (x[c][0] - no.pai.pai.pai.data[c][0])**2

        aux = math.sqrt(aux)
        delta = di[i][i-4]
        if (aux - delta)**2 < 10**(-3):
            return True

        else:
            return False

    else:
        return True

def angulo_entrada(x):
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

def distancia_entrada(x):
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

if __name__ == "__main__":
    
    #Calculo para a protein feb4
    #https://www.rcsb.org/structure/4FEB
    feb4 = protein.feb
    n = len(feb4)
    teta = angulo_entrada(feb4)
    di = distancia_entrada(feb4)

    atomo1 = Node([[-4.975, 1], [-16.627, 2], [-2.799, 4]])
    atomo2 = Node([[-4.88, 1], [-15.165, 2], [-3.047, 4]])
    atomo3 = Node([[-6.106, 1], [-14.656, 2], [-3.8, 4]])

    Molecula = BinaryTree()

    Molecula.root = atomo1
    atomo1.right = atomo2
    atomo2.right = atomo3
    atomo2.pai = atomo1
    atomo3.pai = atomo2

    Molecula.insertion(atomo3, 3)
    Molecula.exibir()