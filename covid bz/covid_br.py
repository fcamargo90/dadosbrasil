from datetime import datetime
import pandas as pd
from covid_br_aux import get_death_data, get_estimated_deaths, get_estimated_deaths_graphics, get_estimation_model,\
    get_moving_average_data, get_new_deaths_graphics, get_population_data


def dateparse(date):
    return datetime.strptime(date, "%d/%m/%Y")


if __name__ == "__main__":

    moving_averate_window = 7

    death_dataframe = pd.read_csv(
        "HIST_PAINEL_COVIDBR_23jul2020_states.csv", converters={"data": dateparse}
    )

    states, dates, new_deaths, cumulative_deaths = get_death_data(death_dataframe)

    population_dataframe = pd.read_csv("populacao.csv", dtype={"Populacao": int})

    population = get_population_data(population_dataframe)

    moving_averages = get_moving_average_data(new_deaths, moving_averate_window)

    model_parameters = get_estimation_model(cumulative_deaths, population)

    estimation_dates, estimated_deaths = get_estimated_deaths(dates, cumulative_deaths, model_parameters)

    new_deaths_graphics = get_new_deaths_graphics(states, dates, new_deaths, moving_averages, moving_averate_window)

    with open("new_deaths.html", "a") as file:
        for state, figure in new_deaths_graphics.items():
            file.write(figure.to_html(full_html=False, include_plotlyjs='cdn'))

    estimated_deaths_gaphics = get_estimated_deaths_graphics(
        states, dates, cumulative_deaths, estimation_dates, estimated_deaths
    )

    with open("estimated_deaths.html", "a") as file:
        for state, figure in estimated_deaths_gaphics.items():
            file.write(figure.to_html(full_html=False, include_plotlyjs='cdn'))
