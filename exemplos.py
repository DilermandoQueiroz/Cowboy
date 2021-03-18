from ga import *
import math

print("__________________________________________________________\n\
TESTANDO O PRODUTO GEOMETRICO NA METRICA EUCLIDIANA R^(3,0)\n\
__________________________________________________________")

a = [[1, 0], [-2, 2], [3, 7]]
b = [[1, 4], [1, 3], [-2, 6]]

print(F'(1 - 2*e2 + e1^e2^e3)(e4 + e1^e2 - 2*e2^e3) = {produto_geometrico(a, b, metrica = Metrica(3,0))}')


print("_________________________________________________________________\n\
TESTANDO O PRODUTO GEOMETRICO NA METRICA PSEUDO-EUCLIDIANA R^(4,1)\n\
__________________________________________________________________")
conforme = Metrica(4, 1)

print('(1)(1) = ',produto_geometrico([[1, 0]], [[1, 0]], metrica=conforme))
for c in range(0, 5):
    print(f"e{c+1}e{c+1} = {produto_geometrico([[1, 2**c]], [[1, 2**c]], metrica=conforme)}")

emais = MultiVetor([[1, 2**3]])
emenos = MultiVetor([[1, 2**4]])
print(f"e+ = {emais}\ne- = {emenos}")

print('(e+ + e-)(e+ + e-) =', produto_geometrico(emais + emenos, emais + emenos, metrica=conforme))
print('(e+ - e-)(e+ - e-) =', produto_geometrico(emais - emenos, emais - emenos, metrica=conforme))

e0 = 0.5*(emais + emenos)
einf = emenos - emais
print(f'e0 = {e0}\nninf = {einf}')

print('e0einf =',produto_geometrico(e0, einf, metrica=conforme))

print("__________________________________________________________\n\
REPRESENTANDO PONTOS NA METRICA CONFORME R^(4,1)\n\
_________________________________________________________")
p2 = MultiVetor([[-1, 1]])
p3 = MultiVetor([[-1.5, 1], [math.sqrt(3)/2, 2]])
p4 = MultiVetor([[-1.311, 1], [1.552, 2], [0.702, 4]])

p_2 = e0 + p2 + 0.5*(p2*p2)*einf
s2 = p_2 - (0.5*(math.sqrt(3)*math.sqrt(3))*einf)

p_3 = e0 + p3 + 0.5*(p3*p3)*einf
s3 = p_3 - (0.5*(1*1)*einf)

p_4 = e0 + p4 + 0.5*(p4*p4)*einf

print(f'p2 = {p_2}\np3 = {p_3}\np4 = {p_4}')
print(f's2 = {s2}\ns3 = {s3}')
print(f's2^s3 = {s2^s3}')

