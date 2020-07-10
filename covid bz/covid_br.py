import pandas as pd
from graficos import plotar_obitos_novos_ma


def moving_average(N, lista):
    cumsum, moving_aves = [0], []

    for i, x in enumerate(lista, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            moving_aves.append(moving_ave)

    return moving_aves


df = pd.read_excel("HIST_PAINEL_COVIDBR_09jul2020_states.xlsx")

datas = dict()
obitos_novos = dict()
obitos_acumulados = dict()
for index, row in df.iterrows():
    estado = row["estado"]
    data = row["data"]
    obiton = row["obitosNovos"]
    obitoa = row["obitosAcumulado"]
    if estado not in datas:
        datas[estado] = [data]
    else:
        datas[estado].append(data)
    if estado not in obitos_novos:
        obitos_novos[estado] = [obiton]
    else:
        obitos_novos[estado].append(obiton)
    if estado not in obitos_acumulados:
        obitos_acumulados[estado] = [obitoa]
    else:
        obitos_acumulados[estado].append(obitoa)

medias_moveis = dict()
for estado in obitos_novos:
    lista_obitos = obitos_novos[estado]
    medias_moveis[estado] = moving_average(7, lista_obitos)

for estado in datas:
    plotar_obitos_novos_ma(estado, datas, obitos_novos, medias_moveis)
