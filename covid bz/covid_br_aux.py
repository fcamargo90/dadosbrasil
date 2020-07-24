from datetime import timedelta
from opt_mystic import estimation, optimize
from graficos_mm import plot_new_deaths
from graficos_est import plot_estimated_deaths


def get_death_data(df):

    df = df.loc[df["obitosAcumulado"] >= 10]

    states = list(df["estado"].unique())
    dates = dict()
    new_deaths = dict()
    cumulative_deaths = dict()

    for state in states:
        dates[state] = []
        new_deaths[state] = []
        cumulative_deaths[state] = []

    for state, date, new_deaths_entry, cumulative_deaths_entry in zip(df["estado"], df["data"], df["obitosNovos"], df["obitosAcumulado"]):
        dates[state].append(date)
        new_deaths[state].append(new_deaths_entry)
        cumulative_deaths[state].append(cumulative_deaths_entry)

    return states, dates, new_deaths, cumulative_deaths


def get_estimation_model(cumulative_deaths, population, save_file=True):
    x0 = [500, 500, 1, 0.1]
    model_parameters = dict()
    # state = "DF"
    for state in cumulative_deaths:
        x, objetive_function_value = optimize(x0, cumulative_deaths[state], population[state])
        model_parameters[state] = list(x)
        if save_file:
            with open(f"./opt/{state}.txt", mode="w") as file:
                file.write(f"{objetive_function_value}\n{model_parameters[state]}")

    return model_parameters


def get_estimated_deaths(dates, cumulative_deaths, model_parameters):
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


def get_estimated_deaths_graphics(states, dates, cumulative_deaths, estimation_dates, estimated_deaths):
    figures = dict()
    for state in states:
        figures[state] = plot_estimated_deaths(
            state, dates[state], cumulative_deaths[state], estimation_dates[state], estimated_deaths[state]
        )
    return figures


def get_moving_average_data(new_deaths, moving_averate_window):
    moving_averages = dict()
    for state in new_deaths:
        deaths_list = new_deaths[state]
        moving_averages[state] = moving_average(moving_averate_window, deaths_list)

    return moving_averages


def get_new_deaths_graphics(states, dates, new_deaths, moving_averages, moving_averate_window):
    figures = dict()
    for state in states:
        figures[state] = plot_new_deaths(
            state, dates[state], new_deaths[state], moving_averages[state], moving_averate_window
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


def get_df_value(df, index_column, index, data_column):
    return df.loc[df[index_column] == index, data_column].values[0]
