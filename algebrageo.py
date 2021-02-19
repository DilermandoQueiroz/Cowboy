import math

'''
Biblioteca implementada por Dilermando

estrutura do multivetor [[coeficiente, base], [coeficiente, base] ...]
base esta representada pelos numeros decimais
ex: e1 = 1
    e2 = 2
    e1^e2 = 3
    e3 = 4
    e1^e3 = 5
    e2^e3 = 6
    e1^e2^e3 = 7 
'''

class Metrica():
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def entrada_diagonal(self, index):
        if index <= self.p:
            return +1
        elif index <= self.p + self.q:
            return -1
        else:
            return 0

    def fator_metrica(self, masc):
        index = 0
        mascr = 1

        while masc != 0:
            if (masc & 1) != 0:
                mascr *= self.entrada_diagonal(index)
            masc >>= 1
            index += 1

        return mascr

'''
Adiciona um elemento a um multevetor = multr
'''
def adicionar(coef,masc,multr):
    multr.append([coef, masc])

    return multr

'''
Soma dois multivetores
'''
def soma(mult1, mult2):
    multr=list()
    aux=aux2=0
    c=k=0

    while(aux != len(mult1) and (aux2 != len(mult2))):
        if mult1[c][1] == mult2[k][1]:
            multr.append([mult1[c][0]+mult2[k][0], mult2[k][1]])
            aux = aux + 1
            aux2 = aux2 + 1
            c = c + 1
            k = k + 1

        elif mult1[c][1] < mult2[k][1]:
            multr.append([mult1[c][0], mult1[c][1]])
            aux = aux + 1
            c = c + 1

        else:
            multr.append([mult2[k][0], mult2[k][1]])
            aux2 = aux2 + 1
            k = k + 1

    if c != len(mult1):
        while c != len(mult1):
            multr.append([mult1[c][0], mult1[c][1]])
            c = c + 1

    if k != len(mult2):
        while k != len(mult2):
            multr.append([mult2[k][0], mult2[k][1]])
            k = k + 1

    multr = analisesoma(multr)

    return multr

'''
Subtrai dois multivetores
'''
def sub(mult1, mult2):
    multr=list()
    aux=aux2=0
    c=k=0

    while (aux != len(mult1) and (aux2 != len(mult2))):
        if mult1[c][1] == mult2[k][1]:
            multr.append([mult1[c][0] - mult2[k][0], mult2[k][1]])
            aux = aux + 1
            aux2 = aux2 + 1
            c = c + 1
            k = k + 1

        elif mult1[c][1] < mult2[k][1]:
            multr.append([mult1[c][0], mult1[c][1]])
            aux = aux + 1
            c = c + 1

        else:
            multr.append([-1*mult2[k][0], mult2[k][1]])
            aux2 = aux2 + 1
            k = k + 1

    if c!=len(mult1):
        while c!=len(mult1):
            multr.append([mult1[c][0], mult1[c][1]])
            c = c + 1

    if k!=len(mult2):
        while k!=len(mult2):
            multr.append([-1*mult2[k][0], mult2[k][1]])
            k = k + 1

    multr=analisesoma(multr)

    return multr

'''
Soma as bases comuns e retira as que tem coeficiente 0
'''
def analisesoma(mult):
    for c in range(0, len(mult)):
        for k in range(c+1, len(mult)):
            if (mult[k][1] == mult[c][1]):
                mult[c][0] = mult[c][0]+mult[k][0]
                mult[k][0] = 0

    multr=list()

    for c in range(0, len(mult)):                               
        if (mult[c][0] != 0):
            multr.append([mult[c][0], mult[c][1]])

    multr.sort(key=sortSecond)

    return multr

def sortSecond(val):
    return val[1]

def sortFirst(val):
    return val[0]


'''
Calcula o produto externo entre dois multivetores -- Não é um produto metrico
'''
def pexterno(mult1,mult2):
    multr = list()
    coef=0
    masc=0

    for c in range(0,len(mult1)):
        for k in range(0,len(mult2)):
            coef,masc = pexterno2(mult1[c][0],mult1[c][1],mult2[k][0],mult2[k][1])
            multr.append([coef, masc])

    multr = analisesoma(multr)

    return multr

def pexterno2(coef1,masc1,coef2,masc2):
    mascr = 0
    coefr = coef1*coef2
    sinal = 0
    if (masc1 & masc2) == 0:
        sinal = reordenacanonica(masc1, masc2)
        mascr = masc1|masc2
        coefr = sinal * coef1 * coef2
    else:
        mascr = 0
        coefr = 0

    return coefr, mascr

'''
Faz a reodernação das bases
ex: e3^e2 -> -e2^e3
'''
def reordenacanonica(masc1,masc2):
    trocas=0
    masc1=masc1>>1
    while masc1!=0:
        trocas=trocas+colisoes(masc1 & masc2)
        masc1=masc1>>1
    if (trocas & 1) == 0:
        sinalr=1
    else:
        sinalr=-1

    return sinalr

def colisoes(masc):
    if masc == 5: 
        masc=4
    elif masc==4:
        masc=3
    elif masc==3:
        masc=2
    elif masc!=0:
        masc=1
    return masc

'''
Calcula o produto regressivo entre dois multivetores
'''
def pregressivo(mult1,mult2):
    multr = list()
    coef = 0
    masc = 0

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef, masc = pregressivo2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1])
            multr.append([coef, masc])

    return multr

def pregressivo2(coef1,masc1,coef2,masc2):
    n=3 #3dimensoes
    mascr=masc1 & masc2
    if (graumasc(masc1)+graumasc(masc2)-graumasc(mascr))==n:
        sinal=reordenacanonica(masc1^mascr,masc2^mascr)
        coefr=sinal*coef1*coef2
    else:
        coefr=0
        mascr=0

    return coefr, mascr

'''
Retorna o grau de um multivetor valido ate 31
'''
def grau(mult):
    aux=0
    for c in range(0,len(mult)):
        if mult[c][1]==0:
            aux=aux+0.1
            gmasc=0.1
        if mult[c][1]==1 or mult[c][1]==2 or mult[c][1]==4 or mult[c][1]==8 or mult[c][1]==16:
            aux = aux + 1
            gmasc=1
        elif mult[c][1]==15 or mult[c][1]==29 or mult[c][1]==27 or mult[c][1]==23 or mult[c][1]==30:
            aux = aux + 4
            gmasc=4
        elif mult[c][1]==3 or mult[c][1]==5 or mult[c][1]==6 or mult[c][1]==9 or mult[c][1]==10 or mult[c][1]==12 or mult[c][1]==17 or mult[c][1]==18 or mult[c][1]==20 or mult[c][1]==24:
            aux = aux + 2
            gmasc=2
        elif mult[c][1]==31:
            aux = aux + 5
            gmasc = 5
        else:
            aux=aux+3
            gmasc=3
    if len(mult)*gmasc!=aux:
        gmasc=-1
    elif gmasc==0.1:
        gmasc=0
    return gmasc

'''
Retorna o grau de uma mascara valido ate 31
'''
def graumasc(masc):
    if masc == 0:
        gmasc=0
    elif masc==1 or masc==2 or masc==4 or masc==8 or masc==16:
        gmasc=1
    elif masc==3 or masc==5 or masc==6 or masc==9 or masc==10 or masc==12 or masc==17 or masc==18 or masc==20 or masc==24:
        gmasc=2
    elif masc==7 or masc==13 or masc==25 or masc==19 or masc==21 or masc==11 or masc==14 or masc==22 or masc==26 or masc==28:
        gmasc=3
    elif masc==15 or masc==29 or masc==27 or masc==23 or masc==30:
        gmasc=4
    elif masc==31:
        gmasc=5
    return gmasc

'''
Calcula o produto geometrico entre dois multivetores,
por padrao a metrica sera R^3
'''
def pgeometrico(mult1, mult2, metrica = Metrica(3, 0)):
    multr = list()
    coef = 0
    masc = 0

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef,masc = pgeometrico2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1], metrica)
            multr.append([coef, masc])

    multr = analisesoma(multr)

    return multr

def pgeometrico2(coef1, masc1, coef2, masc2, metrica):
    sinal = reordenacanonica(masc1, masc2)
    metrica = metrica.fator_metrica(masc1 & masc2)
    coefr = sinal * metrica * coef1 * coef2
    mascr = masc1 ^ masc2

    return coefr, mascr

def fatormetrica(masc1,masc2):
    mascr=1
    return mascr

'''
Retorna os elemetos com grau a do multivetor
'''
def extracaodograu(mult, a):
    multr=list()
    sup=list()
    for c in range(0,len(mult)):
        if a==-1:
            if mult[c][1]>=0:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()
        elif a==0:
            if mult[c][1]==0:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()
        elif a==1:
            if mult[c][1]==1 or mult[c][1]==2 or mult[c][1]==4 or mult[c][1]==8 or mult[c][1]==16:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()
        elif a==2:
            if mult[c][1]==3 or mult[c][1]==5 or mult[c][1]==6 or mult[c][1]==9 or mult[c][1]==10 or mult[c][1]==12 or mult[c][1]==17 or mult[c][1]==18 or mult[c][1]==20 or mult[c][1]==24:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()
        elif a==3:
            if mult[c][1]==7 or mult[c][1]==13 or mult[c][1]==25 or mult[c][1]==19 or mult[c][1]==21 or mult[c][1]==11 or mult[c][1]==14 or mult[c][1]==22 or mult[c][1]==26 or mult[c][1]==28:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()
        elif a==4:
            if mult[c][1]==15 or mult[c][1]==29 or mult[c][1]==27 or mult[c][1]==23 or mult[c][1]==30:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()
        elif a==5:
            if mult[c][1] == 31:
                sup.append(mult[c][0])
                sup.append(mult[c][1])
                multr.append(sup[:])
                sup.clear()

    return multr

'''
Retorna o maior elemento do multivetor
'''

def extracaodograumax(mult):
    maior = max(mult, key=sortSecond)
    maior.remove(maior[0])
    return maior

'''
Calcula o reverso de um multivetor onde a é o grau
'''

def reverso(mult, a):
    mult=extracaodograu(mult, a)
    for c in range(0,len(mult)):
        b = grau([mult[c]])
        if mult[c][1]==0 or mult[c][1]==1:
            fator=1
        else:
            fator = (-1) ** (b*(b - 1)/2)
            mult[c][0]=mult[c][0]*fator
    return mult

def norma2reversa(mult, a):
    mult=extracaodograu(mult, a)
    multrev=reverso(mult, a)
    multr=produtoescalar(mult, multrev)

    return multr

def norma(mult):
    cont = 0

    for c in range(0, len(mult)):
        cont = cont + mult[c][0]*mult[c][0]
    n = cont**(1/2)
    for c in range(0,len(mult)):
        mult[c][0] = (mult[c][0]/n)
    return mult

def bladenormalizado(blade, a):
    bladenorma2=norma2reversa(blade, a)
    blade=extracaodograu(blade, a)
    for c in range(0, len(blade)):
        blade[c][0]=blade[c][0]/(bladenorma2[0][0]**(1/2))
    return blade

def inverso(mult,a):
    multr=list()
    sup=list()
    multrev=reverso(mult, a)
    multnorma2=norma2reversa(mult, a)
    for c in range(0,len(multrev)):
        for k in range(0,len(multnorma2)):
            sup.append(multrev[c][0]/multnorma2[k][0])
            sup.append(multrev[c][1])
            multr.append(sup[:])
            sup.clear()
    return multr

def involucao(mult, a):
    mult=extracaodograu(mult, a)
    for c in range(0,len(mult)):
        mult[c][0]=((-1)**a)*mult[c][0]
    return mult

def contracaoesq(mult1, mult2, metrica = Metrica(3, 0)):
    multr = list()
    coef = 0
    masc = 0

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef, masc = pgeometrico2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1], metrica)
            multr.append([coef, masc])
            multr = extracaodograu(multr, graumasc(mult2[k][1]) - graumasc(mult1[c][1]))

    multr = analisesoma(multr)
    
    return multr

def contracaodir(mult1, mult2, metrica = Metrica(3, 0)):
    multr = list()
    coef = 0
    masc = 0

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef, masc = pgeometrico2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1], metrica)
            multr.append([coef, masc])
            multr = extracaodograu(multr, graumasc(mult1[c][1]) - graumasc(mult2[k][1]))

    multr = analisesoma(multr)

    return multr

def produtoescalar(mult1, mult2, metrica = Metrica(3, 0)):
    multr = list()
    coef = 0
    masc = 0

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef, masc = pgeometrico2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1], metrica)
            multr.append([coef, masc])

    multr = extracaodograu(multr, 0)
    multr = analisesoma(multr)

    return multr

def produtodelta(mult1, mult2, metrica = Metrica(3, 0)):
    multr = list()
    coef = 0
    masc = 0
    
    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef, masc = pgeometrico2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1], metrica)
            multr.append([coef, masc])

    multr = extracaodograumax(multr)
    multr = analisesoma(multr)

    return multr

def projecao(mult, blade, a, b):
    mult=extracaodograu(mult, a)
    blade=extracaodograu(blade, b)
    bladerev=inverso(blade, b)
    contra1=contracaoesq(mult, bladerev)
    vetor=contracaoesq(contra1, blade)

    return vetor

def dual(mult, a, n):
    mult=extracaodograu(mult, a)
    if n==3:
        I=[[-1,7]]
    elif n==4:
        I=[[1,15]]
    elif n==5:
        I=[[-1,31]]
    multr=contracaoesq(mult, I)
    return multr

def produtovetorial(mult1, mult2):
    multr = pexterno(mult1, mult2)
    multr = dual(multr, 2, 3)

    return multr

def desdualizacao(dual, n):
    if n == 3:
        I = [[1, 7]]
    elif n == 4:
        I = [[1, 15]]
    elif n == 5:
        I = [[1, 31]]
    multr=contracaoesq(dual,I)
    return multr

def mascarafatoracao(mult):
    masc=list()
    sup=list()
    sup2=list()
    aux=0
    for c in range(0,len(mult)):
        if mult[c][0] < 0:
            mult[c][0]=mult[c][0]*-1
    mult.sort(key=sortFirst, reverse=True)
    sup.append(mult[0][1])
    while sup[0]!=0:
        if (sup[0]&1)==1:
            sup2.append(1)
            sup2.append(2**aux)
            masc.append(sup2[:])
            sup2.clear()
        aux=aux+1
        sup[0]=sup[0]>>1

    return masc

def fatoracao(blade, a):
    bladeK=blade[:]
    blade=extracaodograu(blade, a)
    masc=mascarafatoracao(blade)
    escalar=norma2reversa(blade, a)
    masck=list()
    sup=list()
    fatores=list()
    for c in range(0,len(escalar)):
        escalar[c][0]=escalar[c][0]**(1/2)
    temp=bladenormalizado(bladeK, a)
    for c in range(0,len(masc)):
        sup.append(masc[c])
        masck.append(sup[:])
        sup.clear()
    for c in range(0,len(masc)-1):
        proj=projecao(masck[c],temp,-1,a)
        fatorj=bladenormalizado(proj, -1)
        print(fatorj)
        fatores.append(fatorj)                              #Exemplo [[[1,1],[7,2]]]
        temp=contracaoesq(inverso(fatorj,-1),temp)
    fatork=bladenormalizado(temp,-1)
    for c in range(0,len(fatork)):
        sup.append(fatork[c][0])
        sup.append(fatork[c][1])
        fatores.append(sup[:])
        sup.clear()
    sup.append(escalar[0][0])
    sup.append(escalar[0][1])
    fatores.append(sup[:])
    sup.clear()                                     #Exemplo: [ [[-3,1],[7,2]], [-1,4], [4,0] ]
    return escalar, fatork, fatores

def reflexao(mult, rotor, n):
    #troquei inverso(multv, grau(mult))
    multv=dual(rotor,(n-1),n)
    multvinverso = inverso(multv, -1)
    multr=pgeometrico(multv, mult)
    multr=pgeometrico(multr, multvinverso)
    for c in range(0,len(multr)):
        aux=multr[c][0]
        aux=aux*-1
        multr[c][0]=aux
    return multr

def rotor(plano, angulo):
    rotacao=list()
    adicionar(math.cos(angulo/2), 0, rotacao)

    for c in range(0,len(plano)):
        aux=math.sin(angulo/2)
        plano[c][0]=plano[c][0]*aux
        adicionar(plano[c][0], plano[c][1], rotacao)

    return rotacao

def angulo(mult1, mult2):
    multr = produtoescalar(mult1, mult2)
    mult1norma = norma2reversa(mult1, -1)
    mult2norma = norma2reversa(mult2, -1)
    angulo = multr[0][0]/math.sqrt(mult1norma[0][0]*mult2norma[0][0])

    return angulo