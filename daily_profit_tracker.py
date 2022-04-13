import pandas as pd
from datetime import datetime, timedelta
from simulator import MarketStrategySimulator
import matplotlib.pyplot as plt


def get_best_ccp_for_strategy():
    ccp_dict = {}
    for i in range(1, 50):
        sim = MarketStrategySimulator(i)
        sim.simulate()
        ccp_dict[i] = sim.simulated_positions["PNL"].sum()
    best_ccp = max(ccp_dict, key=ccp_dict.get)
    return best_ccp


def get_daily_performance(ccp):
    # TODO ccp as parameter will be removed and get_best_ccp_for_strategy method will be called and
    #  ccp parameter will be received from there.
    #  Function will only take from_date, to_date parameters to pass simulator and create range of dates.
    sim = MarketStrategySimulator(ccp)
    sim.simulate()
    simulated_positions_df = sim.simulated_positions
    from_date = datetime(2022, 1, 1)
    to_date = datetime(2022, 4, 12)
    date_range = pd.date_range(from_date, to_date).tolist()

    daily_profit_df = pd.DataFrame(columns=["Date", "PortfolioValue"])
    daily_profit_df.Date = date_range
    daily_profit_df.PortfolioValue = sim.budget

    realized_pnl = 0
    for i in range(len(date_range)):
        next_date = date_range[i] + timedelta(days=1)

        # Get positions which are closed at this day
        today_closed_pos = simulated_positions_df[(simulated_positions_df["ExitDate"] >= date_range[i])
                                                  & (simulated_positions_df["ExitDate"] < next_date)]

        # Get positions which are still open today
        today_s_open_pos = simulated_positions_df[(simulated_positions_df["EnterDate"] < next_date) &
                                                  ((simulated_positions_df["ExitDate"] >= next_date) | (
                                                          simulated_positions_df["ExitDate"] is None))]

        today_s_realized_pnl = today_closed_pos["PNL"].sum()
        realized_pnl += today_s_realized_pnl

        # TODO: Giving 0 right now but we should iterate over today_s_open_pos and
        # TODO: get symbol's this day price to calculate instant profit
        today_s_unrealized_pnl = 0

        daily_profit_df.at[i, "PortfolioValue"] += realized_pnl + today_s_unrealized_pnl

    daily_profit_df["%PortfolioValueChg"] = (daily_profit_df["PortfolioValue"] - sim.budget) / sim.budget * 100

    return daily_profit_df


result = get_daily_performance(ccp=3)
print(result)
plt.plot(result.Date, result["%PortfolioValueChg"])
plt.show()
