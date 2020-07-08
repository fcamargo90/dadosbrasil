from copy import deepcopy
from script2 import mult


def soma(lista):
    resultado = sum(lista)
    return resultado

a = 1
b = a
a = 2
c = [["a"], ["b"], ["c"]]
d = deepcopy(c)

xx = soma([1, 2, 3])

yy = mult([1, 2, 3])
