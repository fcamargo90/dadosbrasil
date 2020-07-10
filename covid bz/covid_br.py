import pandas as pd

df = pd.read_excel("HIST_PAINEL_COVIDBR_09jul2020_states.xlsx")

def moving_average(N, lista):
    cumsum, moving_aves = [0], []

    for i, x in enumerate(lista, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            moving_aves.append(moving_ave)

    return moving_aves

obitos_acumulados=dict()
obitos_novos=dict()
datas=dict()
estado=dict()

for index, row in df.iterrows():
    obiton = row("obitosNovos")
    obitoa = row("obitosAcumulado")
    estado = row("estado")
    data = row("data")

    if estado not in datas:
        datas[estado]=[data]
    else
        datas[estado].append

    if estado not in datas:
        datas[estado] = [data]
    else
        datas[estado].append