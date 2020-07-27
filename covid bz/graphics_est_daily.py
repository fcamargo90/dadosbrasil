import plotly.graph_objects as go


def plot_est_daily_deaths(
        states, estimation_dates, estimated_deaths, estimated_daily_deaths_sates_out
):

    fig1 = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(text=f"Estimated daily deaths by state"),
            xaxis=dict(
                nticks=40,
            ),
            yaxis=dict(
                nticks=20,
            )
        )
    )

    for state in states:
        fig1.add_trace(
            go.Scatter(
                x=estimation_dates[state],
                y=estimated_deaths[state],
                name=f"({state})",
                line=go.scatter.Line(),
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

    with open(estimated_daily_deaths_sates_out, "w") as out:
        fig1.write_html(out)

    return fig1
