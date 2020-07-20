from datetime import timedelta
import pandas as pd
from graficos_mm import plotar_obitos_novos_ma
from graficos_est import plotar_modelos_de_estimacao
from opt_mystic import estimacao, otimiza


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
    if obitoa >= 10:
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
    plotar_obitos_novos_ma(estado, datas[estado], obitos_novos[estado], medias_moveis[estado])

x0 = [500, 500, 1, 0.1]
additional_points = 300
deltat = timedelta(days=1)
datas2 = dict()
estimacoes = dict()
opt_par = dict()
# estado = "DF"
for estado in obitos_acumulados:
    print(estado)
    datas2[estado] = []
    estimacoes[estado] = []
    x, fun_obj = otimiza(obitos_acumulados[estado], x0)
    opt_par[estado] = list(x)
    with open("./opt/results" + estado + ".txt", mode="w") as file:
        file.write(f"{fun_obj}\n{opt_par[estado]}")
    for t in range(len(datas[estado]) + additional_points):
        if t > 0:
            valor = estimacao(x, t)
            if valor / estimacoes[estado][-1] > 1.001:
                estimacoes[estado].append(valor)
                if t < len(datas[estado]):
                    datas2[estado].append(datas[estado][t])
                else:
                    datas2[estado].append(datas2[estado][-1] + deltat)
            else:
                break
        else:
            estimacoes[estado].append(estimacao(x, t))
            datas2[estado].append(datas[estado][t])

for estado in datas:
    plotar_modelos_de_estimacao(estado, datas[estado], datas2[estado], obitos_acumulados[estado], estimacoes[estado])
