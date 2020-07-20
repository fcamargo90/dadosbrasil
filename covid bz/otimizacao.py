from math import exp
from functools import partial, update_wrapper
from pyOpt import Optimization


def getlastsolution(prob: Optimization):
    new_index = prob.firstavailableindex(prob.getSolSet())
    return prob.getSol(new_index - 1)


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
    # f = 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2
    # g = []

    f = funcao_objetivo(x, obitos)
    # g = derivada(x, obitos)
    g = []
    return f, g, 0


def otimiza(obitos, x0):
    a, b, c, d = x0
    partial_func = partial(problema, obitos=obitos)
    update_wrapper(partial_func, problema)

    # Instantiate Optimization Problem
    opt_prob = Optimization('Rosenbrock Unconstraint Problem', partial_func)
    # opt_prob.addVarGroup('x', 2, 'c', lower=-1e10, upper=0.5, value=-3.0)
    # opt_prob.addVar('x1', 'c', lower=-10, upper=10, value=-3.0)
    # opt_prob.addVar('x2', 'c', lower=-10, upper=10, value=-4.0)
    opt_prob.addVar('A', 'c', lower=0, upper=2000, value=a)
    opt_prob.addVar('B', 'c', lower=0, upper=2000, value=b)
    opt_prob.addVar('C', 'c', lower=0, upper=2, value=c)
    opt_prob.addVar('D', 'c', lower=0, upper=1, value=d)
    # opt_prob.addCon('C', type='i', lower=0, upper=5, equal=c)
    # opt_prob.addCon('D', type='i', lower=0, upper=1, equal=d)
    opt_prob.addObj('f')
    # print(opt_prob)

    # from pyOpt.pySLSQP.pySLSQP import SLSQP
    # sopt = SLSQP()
    # sopt.setOption('IPRINT', -1)

    from pyOpt.pySOLVOPT.pySOLVOPT import SOLVOPT
    sopt = SOLVOPT()
    sopt.setOption('iprint', -1)

    [fstr, xstr, inform] = sopt(opt_prob, sens_type='FD')
    solution = getlastsolution(opt_prob)
    print(solution)
    return xstr, solution

# 1054.54695461914/(1+892.295063680813*exp(-(1.15212470711266+0.0687737393848558*x)))
