from functools import partial
from math import exp
from mystic.solvers import diffev2


def estimacao(x, t):
    A, B, C, D = x
    est = A / (1 + B * exp(-(C + D * t)))
    return est


def funcao_objetivo(x, obitos):
    y = []
    for t, nobitos in enumerate(obitos):
        est = estimacao(x, t)
        yt = (nobitos - est)**2
        y.append(yt)
    return sum(y)


def derivada(x, obitos):
    a, b, c, d = x
    deriv_a, deriv_b, deriv_c, deriv_d = ([], [], [], [])
    for i, o in enumerate(obitos):
        deriv_a.append(-(2*(o-a/(b*exp(-d*i-c)+1)))/(b*exp(-d*i-c)+1))
        deriv_b.append((2*a*exp(d*i+c)*(o*b+(exp(c)*o-a*exp(c))*exp(d*i)))/(b+exp(d*i+c))**3)
        deriv_c.append(-(2*a*b*exp(-c-i*d)*(o-a/(b*exp(-c-i*d)+1)))/(b*exp(-c-i*d)+1)**2)
        deriv_d.append(-(2*i*a*b*((exp(c)*o-a*exp(c))*exp(i*d)+b*o)*exp(i*d+c))/(exp(i*d+c)+b)**3)
    return sum(deriv_a), sum(deriv_b), sum(deriv_c), sum(deriv_d)


def problema(x, obitos):

    f = funcao_objetivo(x, obitos)
    # g = derivada(x, obitos)
    # g = []
    return f


def otimiza(obitos, x0):
    partial_func = partial(problema, obitos=obitos)
    result = diffev2(partial_func, x0=x0, npop=10, gtol=200, disp=False, full_output=True, maxiter=300)
    return result[0]
