from functools import partial
from math import exp
from mystic.solvers import diffev2


def constraint(x, population):
    # A <= state_population * 0.5%
    return x[0] - population * 0.005


def estimation(x, t):
    A, B, C, D = x
    est = A / (1 + B * exp(-(C + D * t)))
    return est


def gradient(x, cumulative_deaths):
    a, b, c, d = x
    diff_a, diff_b, diff_c, diff_d = ([], [], [], [])
    for t, deaths in enumerate(cumulative_deaths):
        diff_a.append(-(2*(deaths-a/(b*exp(-d*t-c)+1)))/(b*exp(-d*t-c)+1))
        diff_b.append((2*a*exp(d*t+c)*(deaths*b+(exp(c)*deaths-a*exp(c))*exp(d*t)))/(b+exp(d*t+c))**3)
        diff_c.append(-(2*a*b*exp(-c-t*d)*(deaths-a/(b*exp(-c-t*d)+1)))/(b*exp(-c-t*d)+1)**2)
        diff_d.append(-(2*t*a*b*((exp(c)*deaths-a*exp(c))*exp(t*d)+b*deaths)*exp(t*d+c))/(exp(t*d+c)+b)**3)
    return sum(diff_a), sum(diff_b), sum(diff_c), sum(diff_d)


def objective_function(x, cumulative_deaths):
    y1 = []
    for t, deaths in enumerate(cumulative_deaths):
        est = estimation(x, t)
        yt = (deaths - est)**2
        y1.append(yt)
    # y2 = []
    # for t, deaths in enumerate(moving_averages):
    #     est = time_differential(x, t)
    #     yt = (deaths - est)**2
    #     y2.append(yt)
    # return sum(y1) + sum(y2)
    return sum(y1)


def optimize(x0, cumulative_deaths, population, _):
    partial_func = partial(objective_function, cumulative_deaths=cumulative_deaths)
    # partial_func = partial(objective_function, cumulative_deaths=cumulative_deaths, moving_averages=moving_averages)
    partial_const = partial(constraint, population=population)
    result = diffev2(
        partial_func, x0=x0, penalty=partial_const, npop=10, gtol=200, disp=False, full_output=True, maxiter=300
    )
    return result[0], result[1]


def time_differential(x, t):
    a, b, c, d = x
    diff = (a * b * d * exp(d * t + c)) / (exp(d * t + c) + b) ** 2
    return diff
