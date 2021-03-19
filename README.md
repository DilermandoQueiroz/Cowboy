# Cowboy

Cowboy é uma biblioteca Python para Álgebra Geométrica, ela foi desenvolvida para dar suporte as minhas pesquisas de iniciação cientifica (IC) para auxiliar no Problema de Geometria de Distâncias Molecular (PGDM).

A Álgebra Geométrica é uma boa ferramenta para representar algebricamente os objetos geométricos,  tornando ela uma boa alternativa a Álgebra Linear, sua estrutura é construída baseada no conceito de subespaço vetorial.

Espaços $k$ - dimensionais podem ser expandidos a partir de $k$ vetores linearmente independentes, na Álgebra Geométrica esses subespaços são chamados de $k$-blades onde k é o dimensão do blade. Para o espaço do $\mathbb{R}^3$ sobre uma métrica Euclidiana a base é dada por:
$$
\lbrace 1 , e_1, e_2, e_3, e_1 \wedge e_2, e_1 \wedge e_3,e_2 \wedge e_3 , e_1 \wedge e_2 \wedge e_3 \rbrace
$$

E a combinação linear de seus elementos, chamado de multivetor, tem a estrutura:
$$
M = \eta_1 1 + \eta_2 e_1 + \eta_3 e_2 + \eta_4 e_3 + \eta_5 e_1 \wedge e_2 + \eta_6 e_1 \wedge e_3 + \eta_7 e_2 \wedge e_3 + \eta_8 e_1 \wedge e_2 \wedge e_3.
$$

onde $\eta_i$ sãos os coeficientes.



### Resumo da sintaxe

-------

| Sintaxe  | Operação |
|:-:|:-:|
| + |  soma |
| - |  subtração |
|  ^ | produto externo |
| *  | produto geométrico |
| ~  | inverso |
| <<  | contração a esquerda |


