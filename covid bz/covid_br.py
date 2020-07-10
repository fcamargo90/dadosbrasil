import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    if estado == "RO":
        print(obiton)
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

fig1 = go.Figure(
    layout=go.Layout(
        title=go.layout.Title(text="Médias móveis"),
        xaxis=dict(
            nticks=40,
        ),
        yaxis=dict(
            nticks=20,
        )
    )
)

fig1.add_trace(
    go.Scatter(
        x=datas["RO"],
        y=obitos_novos["RO"],
        name="RO",
        line=go.scatter.Line(color="red"),
    ),
)

fig1.update_layout(
    xaxis_tickformatstops=[
        dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
        dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),
        dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        dict(dtickrange=[86400000, 604800000], value="%d/%m/%Y"),
        dict(dtickrange=[604800000, "M1"], value="%d/%m/%Y"),
        dict(dtickrange=["M1", "M12"], value="%b/%Y"),
        dict(dtickrange=["M12", None], value="%Y")
    ],
)

fig1.write_html("mm_ro.html")
