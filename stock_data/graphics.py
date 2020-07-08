import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_graphics(
        investment_keys, colors, days, selic_anual_interest_rates, brd_usd_exchange_rates, daily_balances,
        volatilities_days, rolling_volatilities, bova11_ivvb11_rates, risk_performance, volatilities, compounded_returns
):

    fig0 = make_subplots(specs=[[{"secondary_y": True}]])

    fig0.add_trace(
        go.Scatter(
            x=days,
            y=selic_anual_interest_rates,
            name="Selic",
        ),
    )

    fig0.add_trace(
        go.Scatter(
            x=days,
            y=brd_usd_exchange_rates,
            line=go.scatter.Line(color="red"),
            name="BRL/USD (RHS)",
        ),
        secondary_y=True,
    )

    fig0.update_layout(
        title=go.layout.Title(text="Macroeconomic variables (Brazil)"),
        xaxis=dict(
            nticks=40,
        ),
        yaxis=dict(
            nticks=20,
        ),
        xaxis_tickformatstops=[
            dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
            dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
            dict(dtickrange=[60000, 3600000], value="%H:%M m"),
            dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
            dict(dtickrange=[86400000, 604800000], value="%d/%m/%Y"),
            dict(dtickrange=[604800000, "M1"], value="%d/%m/%Y"),
            dict(dtickrange=["M1", "M12"], value="%b/%Y"),
            dict(dtickrange=["M12", None], value="%Y"),
        ]
    )

    fig0.write_html("macroeconomic_variables.html")

    fig1 = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(text="Investments Daily Balance"),
            xaxis=dict(
                nticks=40,
            ),
            yaxis=dict(
                nticks=20,
            )
        )
    )

    for key in investment_keys:
        fig1.add_trace(
            go.Scatter(
                x=days,
                y=daily_balances[key],
                name=key,
                line=go.scatter.Line(color=colors[key]),
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
        ]
    )

    fig1.write_html("investments_daily_balance.html")

    fig2 = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(text="Rolling volatilities"),
            xaxis=dict(
                nticks=40,
            ),
            yaxis=dict(
                nticks=20,
            )
        )
    )

    for key in investment_keys:
        fig2.add_trace(
            go.Scatter(
                x=volatilities_days,
                y=rolling_volatilities[key],
                name=key,
                line=go.scatter.Line(color=colors[key]),
            ),
        )

    fig2.update_layout(
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
        yaxis=dict(
            tickformat=".2%",
        ),
    )

    fig2.write_html("rolling_volatilities.html")

    fig3 = go.Figure(
        layout=go.Layout(
            title=go.layout.Title(text="BOVA11/Return rate"),
            xaxis=dict(
                nticks=40,
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[x / 20 for x in list(range(21))],
                range=[0, 1],
                tickformat=".2%",
            ),
        ),
        data=go.Scatter(
            x=days,
            y=bova11_ivvb11_rates,
            line=go.scatter.Line(color="blue"),
        ),
    )

    fig3.update_layout(
        xaxis_tickformatstops=[
            dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
            dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
            dict(dtickrange=[60000, 3600000], value="%H:%M m"),
            dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
            dict(dtickrange=[86400000, 604800000], value="%d/%m/%Y"),
            dict(dtickrange=[604800000, "M1"], value="%d/%m/%Y"),
            dict(dtickrange=["M1", "M12"], value="%b/%Y"),
            dict(dtickrange=["M12", None], value="%Y")
        ]
    )

    fig3.write_html("bova11_ivvb11_rates.html")

    fig4 = go.Figure(
        data=[go.Bar(
            x=investment_keys,
            y=[item for key, item in risk_performance.items()],
            marker_color=[item for key, item in colors.items()]
        )],
        layout=go.Layout(
            title=go.layout.Title(text="Risk Performance (Risk/Return)"),
        )
    )

    # fig4.update_traces(
    #     marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6
    # )

    fig4.write_html("risk_performance.html")

    fig5 = make_subplots(x_title="Risk (%)", y_title="Return (%)")

    for key in investment_keys:
        fig5.add_scatter(
            x=[volatilities[key]],
            y=[compounded_returns[key]],
            mode="markers",
            marker=dict(size=20, color=colors[key]),
            name=key, row=1, col=1
        )

    fig5.update_layout(
        title=go.layout.Title(text="Return X Risk"),
        xaxis=dict(
            tickformat=".2%",
            nticks=30,
            range=[0, 0.3],
        ),
        yaxis=dict(
            tickformat=".2%",
            nticks=20,
        ),
    )

    fig5.write_html("return_risk.html")

    return
