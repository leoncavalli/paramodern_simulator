import pandas as pd
from datetime import datetime, timedelta
from simulator import MarketStrategySimulator


def get_daily_performance(ccp):
    sim = MarketStrategySimulator(ccp)
    sim.simulate()
    simulated_positions_df = sim.simulated_positions
    print(simulated_positions_df)
    from_date = datetime(2022, 3, 1)
    to_date = datetime(2022, 4, 13)
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

        # Giving 0 right now but we should iterate over today_s_open_pos and
        # get symbol's this day price to calculate instant profit
        today_s_unrealized_pnl = 0

        daily_profit_df.at[i, "PortfolioValue"] += realized_pnl + today_s_unrealized_pnl

    daily_profit_df["%PortfolioValueChg"] = (daily_profit_df["PortfolioValue"]-sim.budget)/sim.budget * 100

    return daily_profit_df


print(get_daily_performance(10))
