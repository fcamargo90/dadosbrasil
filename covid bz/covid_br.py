from datetime import datetime
from pathlib import Path
import pandas as pd
from covid_br_aux import get_death_data, get_estimated_cumulative_deaths, get_estimated_daily_deaths,\
    get_estimation_model, get_moving_average_data, get_population_data, plot_graphics


def dateparse(date):
    return datetime.strptime(date, "%d/%m/%Y")


if __name__ == "__main__":

    daily_deaths_sates_out = Path("daily_states_deaths.html")

    estimated_daily_deaths_sates_out = Path("estimated_daily_deaths_sates.html")

    cumulative_deaths_states_out = Path("cumulative_states_deaths.html")

    estimated_cumulative_deaths_states_out = Path("estimated_cumulative_states_deaths.html")

    moving_averate_window = 7

    death_dataframe = pd.read_csv(
        "HIST_PAINEL_COVIDBR_23jul2020_states.csv", converters={"data": dateparse}
    )

    states, dates, daily_deaths, cumulative_deaths = get_death_data(death_dataframe)

    population_dataframe = pd.read_csv("populacao.csv", dtype={"Populacao": int})

    population = get_population_data(population_dataframe)

    moving_averages = get_moving_average_data(daily_deaths, moving_averate_window)

    model_parameters = get_estimation_model(cumulative_deaths, population, moving_averages)

    dates_estimated_daily_deaths, estimated_daily_deaths = \
        get_estimated_daily_deaths(dates, daily_deaths, model_parameters)

    dates_estimated_cumulative_deaths, estimated_cumulative_deaths = \
        get_estimated_cumulative_deaths(dates, cumulative_deaths, model_parameters)

    plot_graphics(
        states, dates, daily_deaths, moving_averages, dates_estimated_daily_deaths,
        estimated_daily_deaths, moving_averate_window, cumulative_deaths, dates_estimated_cumulative_deaths,
        estimated_cumulative_deaths, daily_deaths_sates_out, estimated_daily_deaths_sates_out,
        cumulative_deaths_states_out, estimated_cumulative_deaths_states_out
    )
