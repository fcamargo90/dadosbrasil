import math
import statistics
import pandas as pd
from graphics import plot_graphics

df = pd.read_excel(r"Stock data v1.1.xlsm", skiprows=list(range(0, 8)), dtype={})

days = df.iloc[:, 1].to_list()
selic_anual_interest_rates = df.iloc[:, 5].to_list()
ibovespa_stock_price_indices = df.iloc[:, 3].to_list()
sep500_stock_price_indices = df.iloc[:, 2].to_list()
brd_usd_exchange_rates = df.iloc[:, 4].to_list()

invest0 = 1.0
annual_commercial_days = 252
selic_correction = 0.1
bova11_combined_rate = 0.2
rolling_volatilities_window = 21

investment_keys = ["Selic", "BOVA11", "IVVB11", "BOVA11 + IVVB11"]
colors = {"Selic": "blue", "BOVA11": "gray", "IVVB11": "red", "BOVA11 + IVVB11": "green"}

sqrt_annual_commercial_days = math.sqrt(annual_commercial_days)

daily_balances = dict()
bova11_ivvb11_rates = [bova11_combined_rate]
for key in investment_keys:
    daily_balances[key] = [invest0]
    if key == "Selic":
        for rate in selic_anual_interest_rates[1:]:
            last_balance = daily_balances[key][-1]
            new_balance = last_balance * (1 + (rate - selic_correction) / 100) ** (1 / annual_commercial_days)
            daily_balances[key].append(new_balance)
    elif key == "BOVA11":
        index0 = ibovespa_stock_price_indices[0]
        for index in ibovespa_stock_price_indices[1:]:
            last_balance = daily_balances[key][-1]
            new_balance = index / index0 * last_balance
            daily_balances[key].append(new_balance)
            index0 = index
    elif key == "IVVB11":
        index0 = sep500_stock_price_indices[0]
        exchange_rate0 = brd_usd_exchange_rates[0]
        for index, exchange_rate in zip(sep500_stock_price_indices[1:], brd_usd_exchange_rates[1:]):
            last_balance = daily_balances[key][-1]
            new_balance = (index * exchange_rate) / (index0 * exchange_rate0) * last_balance
            daily_balances[key].append(new_balance)
            index0 = index
            exchange_rate0 = exchange_rate
    elif key == "BOVA11 + IVVB11":
        ivvb11_combined_rate = 1 - bova11_combined_rate
        for bova11_balance, ivvb11_balance in zip(daily_balances["BOVA11"][1:], daily_balances["IVVB11"][1:]):
            bova11_fraction = bova11_combined_rate * bova11_balance
            ivvb11_fraction = ivvb11_combined_rate * ivvb11_balance
            new_balance = bova11_fraction + ivvb11_fraction
            daily_balances[key].append(new_balance)
            bova11_ivvb11_rates.append(bova11_fraction / new_balance)

daily_returns = dict()
for key in investment_keys:
    daily_returns[key] = []
    daily_balance0 = daily_balances[key][0]
    for daily_balance in daily_balances[key][1:]:
        daily_return = daily_balance/daily_balance0 - 1
        daily_returns[key].append(daily_return)
        daily_balance0 = daily_balance

volatilities = dict()
compounded_returns = dict()
risk_performance = dict()
for key in investment_keys:
    volatilities[key] = statistics.stdev(daily_returns[key])*sqrt_annual_commercial_days
    future_value = daily_balances[key][-1]
    compounded_returns[key] = future_value**(annual_commercial_days/len(daily_returns[key]))-1
    risk_performance[key] = volatilities[key]/compounded_returns[key]

volatilities_days = days[rolling_volatilities_window + 1:]
rolling_volatilities = dict()
for key in investment_keys:
    rolling_volatilities[key] = []
    for i in range(rolling_volatilities_window, len(daily_returns[key])):
        daily_returns_window = daily_returns[key][i - rolling_volatilities_window:i]
        volatility = statistics.stdev(daily_returns_window)*sqrt_annual_commercial_days
        rolling_volatilities[key].append(volatility)

plot_graphics(
        investment_keys, colors, days, selic_anual_interest_rates, brd_usd_exchange_rates, daily_balances,
        volatilities_days, rolling_volatilities, bova11_ivvb11_rates, risk_performance, volatilities, compounded_returns
)
