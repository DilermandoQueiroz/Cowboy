# Cowboy

Cowboy é uma biblioteca Python para Álgebra Geométrica, ela foi desenvolvida para dar suporte as minhas pesquisas de iniciação cientifica (IC) para auxiliar no Problema de Geometria de Distâncias Molecular (PGDM).

A Álgebra Geométrica é uma boa ferramenta para representar algebricamente os objetos geométricos,  tornando ela uma boa alternativa a Álgebra Linear, sua estrutura é construída baseada no conceito de subespaço vetorial.

Algumas das interpretações geométricas:

![](https://upload.wikimedia.org/wikipedia/commons/2/27/N_vector_positive.svg)


### Estrutura do multivetor

----

O multivetor pode ser inicializado como:

```python
from cowboy import *  # import cowboy

# cria um multivetor vazio
a = MultiVetor()

# cria um multivetor que é um escalar
b = MultiVetor(5)

# cria o multivetor 5 + 3*e1 + 1*e1^e2
c = MultiVetor([[5, 0], [3, 1], [1, 3]])
```

### Resumo da sintaxe

-------

| Sintaxe  | Operação |
|:-:|:-:|
| + |  soma |
| - |  subtração |
|  ^ | produto externo |
| *  | produto geométrico |
| / | produto geométrico inverso |
| ~  | reverso |
| <<  | contração a esquerda |

### Exemplos de uso

```python
from cowboy import *

a = MultiVetor([[1, 1], [1, 2]]) # a = 1*e1 + 1*e2
b = MultiVetor([[1, 7]]) # b = 1*e1^e2^e3

soma = a+a+b # soma = 2*e1 + 2*e2 + e1^e2^e3

pg = a*b # pg = -e1^e3 + e2^e3

b = a # b = 1*e1 + 1*e2
a = MultiVetor([[1, 1], [1, 4]]) # a = 1*e1 + 1*e2
c = MultiVetor([[1, 4]]) # c = 1*e3

lcont = c << (a ^ b) # lcont = 1*e1 + 1*e2

base = lcont + [[1, 7]] # lcont = 1*e1 + 1*e2 + 1*e1^e2^e3

reverso = ~base # reverso = 1*e1 + 1*e2 - 1*e1^e2^e3

```

