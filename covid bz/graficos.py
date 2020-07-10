from pathlib import Path
import plotly.graph_objects as go
# from plotly.subplots import make_subplots


def plotar_obitos_novos_ma(estado, datas, obitos_novos, medias_moveis):
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
            x=datas[estado],
            y=obitos_novos[estado],
            name="Óbitos novos",
            line=go.scatter.Line(color="blue"),
        ),
    )

    fig1.add_trace(
        go.Scatter(
            x=datas[estado][6:],
            y=medias_moveis[estado],
            name="Médias móveis",
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

    fig1.write_html(r"./mm/" + estado + ".html")

    return
