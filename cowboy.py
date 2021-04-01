# Biblioteca implementada por Dilermando Queiroz Neto
# utilizando o livro

# Álgebra Geométrica e Aplicações
#    Fernandes, L. A. F.; Lavor, C.; Oliveira, M. M.
#
#    Sociedade Brasileira de Matemática Aplicada e Computacional (SBMAC)
#    Notas em Matemática Aplicada (NoMA), Volume 85, 2017
#
#    ISSN: 2175-3385 | e-ISSN: 2236-5915
#    ISBN: 978-85-8215-081-8 | e-ISBN: 978-85-8215-080-1
#
#    http://www.ic.uff.br/algebrageometrica

# This Python file uses the following encoding: utf-8

import math
from copy import deepcopy

class Metrica():
    '''Metrica ortogonal com assinatura p,q.
    '''
    def __init__(self, p, q):
        '''Construtor padrao
        '''
        assert isinstance(p, int) and p >= 0
        assert isinstance(q, int) and q >= 0

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
        '''Retorna o fator de metrica computado para uma base dada
        '''
        index = 1
        mascr = 1
        
        while masc != 0:
            if (masc & 1) != 0:
                mascr *= self.entrada_diagonal(index)
            masc >>= 1
            index += 1  

        return mascr

DEFAULT_METRIC = Metrica(4, 1)  # Default metric.

class MultiVetor():
    '''Combinação linear de elementos da base de um espaço multivetorial
    
    A base esta representada pelos numeros decimais
    ex: e1 = 1
    e2 = 2
    e1^e2 = 3
    e3 = 4
    e1^e3 = 5 
    e2^e3 = 6
    e1^e2^e3 = 7 
    '''
    def __init__(self, arg = None):
        '''MultiVetor(),
           MultiVetor(escalar),
           MultiVetor([[coeficiente, mascara], [coeficiente, mascara], ...])
        '''
        if arg == None or arg == 0:
            self.componentes = []
        elif type(arg) == type(1) or type(arg) == type(1.5):
            self.componentes = [[arg, 0]]
        elif type(arg) is type(list()):
            self.componentes = sorted(arg, key = lambda comp: comp[1])
        else:
            raise ValueError
    
    def __add__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)
        return soma(self, mult2)

    def __radd__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)
        return soma(mult2, self)

    def __sub__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)
        return sub(self, mult2)

    __rsub__ = __sub__

    def __sub__(self, mult2):
        return sub(self, mult2)

    def __xor__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)

        return produto_externo(self, mult2)
    
    __rxor__ = __xor__

    def __mul__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)
        return produto_geometrico(self, mult2)
    
    def __rmul__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)
        return produto_geometrico(mult2, self)

    def __invert__(self):
        return reverso(self)

    def __lshift__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)
        return contracao_esquerda(self, mult2)

    def __truediv__(self, mult2):
        if not isinstance(mult2, MultiVetor):
            mult2 = MultiVetor(mult2)

        mult2 = inverso(mult2)
        
        return produto_geometrico(self, inverso(mult2))

    def __float__(self):
        if is_escalar(self):
            return float(self.componentes[0][0])
        else:
            raise ValueError("nao eh um escalar")
    
    
    def __str__(self):
        '''str(self)
        '''
        result = str()
        primeiro_componente = True
        componentes = deepcopy(self.componentes)
        
        for item in componentes:
            if item[0] != 0:
                if primeiro_componente:
                    if item[0] < 0:
                        result += '-'
                    primeiro_componente = False
                else:
                    if item[0] < 0:
                        result += ' - '
                    else:
                        result += ' + '

            if item[1] == 0 or abs(item[0]) != 1:
                result += str(abs(item[0]))

            if item[1] != 0:
                if abs(item[0]) != 1:
                    result += '*'

                index = 1
                primeiro_componente = True
                while item[1] != 0:
                    if (item[1] & 1) != 0:
                        if not primeiro_componente:
                            result += '^'
                        result += 'e%d' %index
                        primeiro_componente = False
                    index += 1
                    item[1] >>= 1

        if primeiro_componente:
            return str(0)

        else:
            return result

def soma(mult1, mult2):
    '''Soma dois multivetores
    '''
    if isinstance(mult1, MultiVetor):
        mult1 = mult1.componentes
    if isinstance(mult2, MultiVetor):
        mult2 = mult2.componentes

    multr = list()
    aux = aux2 = 0
    c = k = 0

    while(aux != len(mult1) and (aux2 != len(mult2))):
        if mult1[c][1] == mult2[k][1]:
            multr.append([mult1[c][0] + mult2[k][0], mult2[k][1]])
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

    return MultiVetor(multr)

def sub(mult1, mult2):
    '''Subtrai dois multivetores
    '''
    if isinstance(mult1, MultiVetor):
        mult1 = mult1.componentes
    if isinstance(mult2, MultiVetor):
        mult2 = mult2.componentes

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

    return MultiVetor(multr)

def analisesoma(mult):
    '''Soma as bases comuns e retira as que tem coeficiente 0
    '''
    for c in range(0, len(mult)):
        for k in range(c+1, len(mult)):
            if (mult[k][1] == mult[c][1]):
                mult[c][0] = mult[c][0]+mult[k][0]
                mult[k][0] = 0

    multr=list()

    for c in range(0, len(mult)):                               
        if (mult[c][0] != 0):
            multr.append([mult[c][0], mult[c][1]])

    sorted(multr, key = lambda comp: comp[1])

    return multr

def produto_externo(mult1, mult2):
    '''Calcula o produto externo entre dois multivetores -- Não é um produto metrico
    '''
    if isinstance(mult1, MultiVetor):
        mult1 = mult1.componentes
    if isinstance(mult2, MultiVetor):
        mult2 = mult2.componentes

    multr = list()

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef,masc = pexterno2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1])
            multr.append([coef, masc])

    multr = analisesoma(multr)

    return MultiVetor(multr)

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

def reordenacanonica(masc1, masc2):
    '''Faz a reodernação das bases
    ex: e3^e2 -> -e2^e3
    '''
    trocas = 0
    masc1 = masc1 >> 1
    
    while masc1 != 0:
        trocas = trocas + colisoes(masc1 & masc2)
        masc1 = masc1 >> 1
    if (trocas & 1) == 0:
        return 1
    else:
        return -1

def colisoes(mask):
    mask = mask - ((mask >> 1) & 0x55555555)
    mask = (mask & 0x33333333) + ((mask >> 2) & 0x33333333)
    return (((mask + (mask >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

def produto_regressivo(mult1,mult2):
    '''Calcula o produto regressivo entre dois multivetores
    '''
    if isinstance(mult1, MultiVetor):
        mult1 = mult1.componentes
    if isinstance(mult2, MultiVetor):
        mult2 = mult2.componentes

    multr = list()

    for c in range(0, len(mult1)):
        for k in range(0, len(mult2)):
            coef, masc = pregressivo2(mult1[c][0], mult1[c][1], mult2[k][0], mult2[k][1])
            multr.append([coef, masc])

    multr = analisesoma(multr)

    return MultiVetor(multr)

def pregressivo2(coef1,masc1,coef2,masc2):
    n=3 #3dimensoes
    mascr=masc1 & masc2
    if (graumasc(masc1)+graumasc(masc2)-graumasc(mascr)) == n:
        sinal=reordenacanonica(masc1^mascr,masc2^mascr)
        coefr=sinal*coef1*coef2
    else:
        coefr=0
        mascr=0

    return coefr, mascr

def __pg(mult1, mult2, metrica = DEFAULT_METRIC, keep = True):
    '''Calcula o produto geometrico entre dois multivetores,
    por padrao a metrica é p=3, q=0
    '''
    if isinstance(mult1, MultiVetor):
        mult1 = mult1.componentes
    if isinstance(mult2, MultiVetor):
        mult2 = mult2.componentes

    multr = list()

    for blade in mult1:
        for blade2 in mult2:
            mascr = blade[1] ^ blade2[1]
            if keep(blade[1], blade2[1], mascr):
                coef, masc = __pg2(blade[0], blade[1], blade2[0], blade2[1], metrica)
                multr.append([coef, masc])

    multr = analisesoma(multr)

    return MultiVetor(multr)

def __pg2(coef1, masc1, coef2, masc2, metrica):
    sinal = reordenacanonica(masc1, masc2)
    metrica = metrica.fator_metrica(masc1 & masc2)
    coefr = sinal * metrica * coef1 * coef2
    mascr = masc1 ^ masc2

    return coefr, mascr

def produto_geometrico(mult1, mult2, metrica = DEFAULT_METRIC):
    """Produto geometrico
    """
    return __pg(mult1, mult2, metrica, lambda masc1, masc2, mascr: True)

def produto_escalar(mult1, mult2, metrica = DEFAULT_METRIC):
    '''O produto escalar estende o produto interno de vetores para subespaços tendo a mesma dimensionalidade.
    Quando utilizados na multiplicação de blades com dimensionalidades diferentes, o resultado é zero.
    '''
    return __pg(mult1, mult2, metrica, lambda masc1, masc2, mascr: mascr == 0)

def contracao_esquerda(mult1, mult2,  metrica = DEFAULT_METRIC):
    '''Contracao a esquerda
    '''
    return __pg(mult1, mult2, metrica, lambda masc1, masc2, mascr: mascr == (-masc1 + masc2))

def contracao_direita(mult1, mult2, metrica = DEFAULT_METRIC):
    '''Contracao a direita
    '''
    return __pg(mult1, mult2, metrica, lambda masc1, masc2, mascr: mascr == (masc1 - masc2))

def produtodelta(mult1, mult2, metrica = DEFAULT_METRIC):
    """Calcula o produto delta entre dois multivetores
    """
    return extracao_graumax(produto_geometrico(mult1, mult2, metrica = metrica))

def produto_vetorial(mult1, mult2):
    """Produto vetorial da algebra vetorial
    """
    return dual(produto_externo(mult1, mult2))

def grau(mult, maximo = False):
    '''Retorna o grau de um multivetor
    '''
    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    aux = 0
    maior = -1
    menor = -1

    for blade in mult:
        grau_masc = graumasc(blade[1])
        if grau_masc > maior:
            maior = grau_masc
        if grau_masc < menor or menor == -1:
            menor = grau_masc
    
    if maximo == False:
        if maior == menor:
            return maior
        else:
            return -1
    else:
        return maior

def graumasc(masc):
    '''Retorna o grau de um blade
    '''
    grau = 0
    while masc != 0:
        if (masc & 1) != 0:
            grau += 1
        masc >>= 1    

    return grau

def extracao_grau(mult, a = -1):
    '''Retorna do mult os blades que possuem o grau a
    '''
    if a != -1:
        multr=list()
        if isinstance(mult, MultiVetor):
            mult = mult.componentes    

        for blade in mult:
            if a == graumasc(blade[1]):
                multr.append(blade)

    else:
        return mult

    return MultiVetor(multr)

def extracao_graumax(mult):
    '''Retorna os blades com maior grau no multivetor
    '''
    if isinstance(mult, MultiVetor):
        mult = mult.componentes
    
    multr = list()
    maior = grau(mult, maximo = True)
    
    for blade in mult:
        if graumasc(blade[1]) == maior:
            multr.append(blade)

    return MultiVetor(multr)

def reverso(mult, a = -1):
    '''Calcula o reverso de um multivetor onde a é o grau
    '''
    if isinstance(mult, MultiVetor):
        mult = mult.componentes
    
    mult = deepcopy(mult)

    if a != -1:
        mult = extracao_grau(mult, a)

    for blade in mult:
        g = graumasc(blade[1])
        if g != 0 and g != 1:
            fator = (-1) ** (g * (g - 1) / 2)
            blade[0] = blade[0]*fator
    
    if type(mult) is type(MultiVetor):
        return mult
    else:
        return MultiVetor(mult)

def norma_reversa_2(mult, a = -1):
    """Calcula o quadrado da norma reversa
    """
    if a != -1:
        mult = extracao_grau(mult, a)
    
    multrev = reverso(mult, a)
    multr = produto_escalar(mult, multrev)

    if not multr.componentes:
        return ValueError("blade nulo")

    return multr

def norma(mult):
    """Retorna o mult normalizado
    """
    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    multr = list()    
    cont = 0

    for blade in mult:
        cont = cont + blade[0] * blade[0] 
    for blade in mult:
        multr.append([blade[0] / (cont**(1/2)), blade[1]])

    return MultiVetor(multr)

def mult_normalizado(mult, a = -1):
    """Retorna o mult normalizado
    """
    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    norma = norma_reversa_2(mult, a)
    norma2 = norma.componentes[0][0]

    multr = list()

    for blade in mult:
        multr.append([blade[0] / (norma2**(1/2)), blade[1]])

    return MultiVetor(multr)

def inverso(mult, a = -1):
    """Calcula o inverso de um mult
    """
    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    multr = list()
    mult_rev = reverso(mult, a)
    mult_rev = mult_rev.componentes
    mult_norma_2 = norma_reversa_2(deepcopy(mult), a)
    norma_2 = mult_norma_2.componentes[0][0]
    

    for blade in mult_rev:
        multr.append([blade[0] / norma_2, blade[1]])
    
    return MultiVetor(multr)

def involucao(mult):
    """A operação de involução de um mult exibe o padrão + − + − + −
    """
    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    multr = list()

    for blade in mult:
        multr.append([((-1)**(graumasc(blade[1]))) * blade[0]  ,blade[1]])
    
    return MultiVetor(multr)

def projecao(mult1, vetor, metrica = Metrica(3,0), a = -1):
    """Faz a projecao de um vetor b para um multivetor qualquer 
    """ 
    if a != -1:
        mult1 = extracao_grau(mult1, a)

    return contracao_esquerda(contracao_esquerda(vetor, mult1), inverso(mult1))

def dual(mult, a = -1):
    """o dual de um mult é dado por seu complemento ortogonal de dimensionalidade (n − k)
    """
    if a != -1:
        mult = extracao_grau(mult, a)

    n = grau(mult, maximo = True)
    i = inverso([[1, (2**n)-1]])

    return contracao_esquerda(mult, i)

def rotor(mult, angulo):
    """gera um Rotor que codifica uma rotação de φ radianos no blade unitario
    """
    rotor = list()
    rotor.append([math.cos(angulo/2), 0])

    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    aux = math.sin(angulo/2)
    for blade in mult:
        rotor.append([blade[0]*aux, blade[1]])

    return MultiVetor(rotor)

def reflexao(vetor, plano):
    """Realiza a reflexao de um vetor em relacao a um plano
    """
    multr = produto_geometrico(produto_geometrico(plano, vetor), inverso(plano))
    for blade in multr.componentes:
        blade[0] = blade[0]*-1
    
    return multr 

def angulo(mult1, mult2):
    multr = produto_escalar(mult1, mult2)
    mult1norma = norma_reversa_2(mult1, -1)
    mult2norma = norma_reversa_2(mult2, -1)
    angulo = multr[0][0]/math.sqrt(mult1norma[0][0]*mult2norma[0][0])

    return angulo

def base(mult):
    """Extrai a base que forma o multivetor
    """
    if isinstance(mult, MultiVetor):
        mult = mult.componentes

    bits = 0
    for blade in mult:
        bits ^= blade[1]

    i = 0
    result = []
    while bits != 0:
        if (bits & 1) == 1:
            result.append([1, 2**i])
        bits >>= 1
        i += 1

    return MultiVetor(result)

def is_escalar(mult):
    if isinstance(mult, MultiVetor):
        if len(mult.componentes) == 1 and mult.componentes[0][1] == 0:
            return True
        else:
            return False
    else:
        raise ValueError("não é um multivetor")