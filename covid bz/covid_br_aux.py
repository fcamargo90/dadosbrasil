from datetime import timedelta
import os
from opt_mystic import estimation, optimize, time_differential
from graphics_daily import plot_daily_deaths
from graphics_cumu import plot_cumulative_deaths
from graphics_est_daily import plot_est_daily_deaths
from graphics_est_cumu import plot_est_cumu_deaths


def get_death_data(df):

    df = df.loc[df["obitosAcumulado"] >= 10]

    states = list(df["estado"].unique())
    dates = dict()
    daily_deaths = dict()
    cumulative_deaths = dict()

    for state in states:
        dates[state] = []
        daily_deaths[state] = []
        cumulative_deaths[state] = []

    for state, date, daily_deaths_entry, cumulative_deaths_entry in\
            zip(df["estado"], df["data"], df["obitosNovos"], df["obitosAcumulado"]):
        dates[state].append(date)
        daily_deaths[state].append(daily_deaths_entry)
        cumulative_deaths[state].append(cumulative_deaths_entry)

    return states, dates, daily_deaths, cumulative_deaths


def get_estimation_model(cumulative_deaths, population, moving_averages, save_file=True):
    x0 = [500, 500, 1, 0.1]
    model_parameters = dict()
    # state = "DF"
    for state in cumulative_deaths:
        x, objetive_function_value = optimize(x0, cumulative_deaths[state], population[state], moving_averages[state])
        model_parameters[state] = list(x)
        if save_file:
            with open(f"./opt/{state}.txt", mode="w") as file:
                file.write(f"{objetive_function_value}\n{model_parameters[state]}")

    return model_parameters


def get_estimated_cumulative_deaths(dates, cumulative_deaths, model_parameters):
    maximum_additional_points = 300
    deltat = timedelta(days=1)
    estimation_dates = dict()
    estimated_deaths = dict()
    for state in cumulative_deaths:
        estimation_dates[state] = []
        estimated_deaths[state] = []
        x = model_parameters[state]
        for t in range(len(dates[state]) + maximum_additional_points):
            if t > 0:
                estimated_value = estimation(x, t)
                if estimated_value / estimated_deaths[state][-1] > 1.001:
                    estimated_deaths[state].append(estimated_value)
                    if t < len(dates[state]):
                        estimation_dates[state].append(dates[state][t])
                    else:
                        estimation_dates[state].append(estimation_dates[state][-1] + deltat)
                else:
                    break
            else:
                estimated_deaths[state].append(estimation(x, t))
                estimation_dates[state].append(dates[state][t])

    return estimation_dates, estimated_deaths


def get_estimated_daily_deaths(dates, daily_deaths, model_parameters):
    maximum_additional_points = 300
    deltat = timedelta(days=1)
    estimation_dates = dict()
    estimated_deaths = dict()
    for state in daily_deaths:
        estimation_dates[state] = []
        estimated_deaths[state] = []
        x = model_parameters[state]
        est0 = 0.1
        for t in range(len(dates[state]) + maximum_additional_points):
            estimated_value = time_differential(x, t)
            if not estimated_deaths[state]:
                est0 = estimated_value
            if estimated_value >= est0:
                estimated_deaths[state].append(estimated_value)
                if t < len(dates[state]):
                    estimation_dates[state].append(dates[state][t])
                else:
                    estimation_dates[state].append(estimation_dates[state][-1] + deltat)
            else:
                break

    return estimation_dates, estimated_deaths


def get_cumulative_deaths_graphics(states, dates, cumulative_deaths, estimation_dates, estimated_deaths):
    figures = dict()
    for state in states:
        figures[state] = plot_cumulative_deaths(
            state, dates[state], cumulative_deaths[state], estimation_dates[state], estimated_deaths[state]
        )
    return figures


def get_moving_average_data(daily_deaths, moving_averate_window):
    moving_averages = dict()
    for state in daily_deaths:
        deaths_list = daily_deaths[state]
        moving_averages[state] = moving_average(moving_averate_window, deaths_list)

    return moving_averages


def get_daily_deaths_graphics(
        states, dates, daily_deaths, moving_averages, estimation_dates, estimated_deaths, moving_averate_window
):
    figures = dict()
    for state in states:
        figures[state] = plot_daily_deaths(
            state, dates[state], daily_deaths[state], moving_averages[state], estimation_dates[state],
            estimated_deaths[state], moving_averate_window
        )

    return figures


def get_population_data(df):
    pop_dict = dict()
    for state, population in zip(df["Estado"], df["Populacao"]):
        pop_dict[state] = population

    return pop_dict


def moving_average(N, lista):
    cumsum, moving_aves = [0], []

    for i, x in enumerate(lista, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            moving_aves.append(moving_ave)

    return moving_aves


def plot_graphics(
        states, dates, daily_deaths, moving_averages, dates_estimated_daily_deaths,
        estimated_daily_deaths, moving_averate_window, cumulative_deaths, dates_estimated_cumulative_deaths,
        estimated_cumulative_deaths, daily_deaths_sates_out, estimated_daily_deaths_sates_out,
        cumulative_deaths_states_out, estimated_cumulative_deaths_states_out
):
    daily_deaths_graphics = get_daily_deaths_graphics(
        states, dates, daily_deaths, moving_averages, dates_estimated_daily_deaths,
        estimated_daily_deaths, moving_averate_window
    )

    if daily_deaths_sates_out.is_file():
        os.remove(daily_deaths_sates_out)

    with open(daily_deaths_sates_out, "a") as file:
        for state, figure in daily_deaths_graphics.items():
            file.write(figure.to_html(full_html=False, include_plotlyjs='cdn'))

    cumulative_deaths_gaphics = get_cumulative_deaths_graphics(
        states, dates, cumulative_deaths, dates_estimated_cumulative_deaths, estimated_cumulative_deaths
    )

    if cumulative_deaths_states_out.is_file():
        os.remove(cumulative_deaths_states_out)

    with open(cumulative_deaths_states_out, "a") as file:
        for state, figure in cumulative_deaths_gaphics.items():
            file.write(figure.to_html(full_html=False, include_plotlyjs='cdn'))

    plot_est_daily_deaths(
        states, dates_estimated_daily_deaths, estimated_daily_deaths, estimated_daily_deaths_sates_out
    )

    plot_est_cumu_deaths(
        states, dates_estimated_cumulative_deaths, estimated_cumulative_deaths, estimated_cumulative_deaths_states_out
    )

    return
