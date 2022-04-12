import pandas as pd
from datetime import datetime, timedelta
from simulator import MarketStrategySimulator

simulator = MarketStrategySimulator(2)
simulator.simulate()
simulated_positions_df = simulator.simulated_positions

simulated_positions_df.EnterDate = simulated_positions_df.EnterDate.apply \
    (lambda enter_date: datetime.strptime(enter_date, "%Y-%m-%dT%H:%M:%S.%fZ"))
simulated_positions_df.ExitDate = simulated_positions_df.ExitDate.apply \
    (lambda enter_date: datetime.strptime(enter_date, "%Y-%m-%dT%H:%M:%S.%fZ"))

from_date = datetime(2022, 3, 11)
to_date = datetime(2022, 4, 11)
date_range = pd.date_range(from_date, to_date).tolist()

daily_profit_df = pd.DataFrame(columns=["Date", "PortfolioValue"])
daily_profit_df.Date = date_range

realized_pnl = 0
for i in range(len(date_range)):
    next_date = date_range[i] + timedelta(days=1)

    # Get positions which are opened at this day
    today_opened_pos = simulated_positions_df[(simulated_positions_df["EnterDate"] >= date_range[i])
                                              & (simulated_positions_df["EnterDate"] < next_date)]

    # Get positions which are closed at this day
    today_closed_pos = simulated_positions_df[(simulated_positions_df["ExitDate"] >= date_range[i])
                                              & (simulated_positions_df["ExitDate"] < next_date)]

    # Check positions opened at this day but closed in next days so still open for now
    today_s_open_pos = today_opened_pos[today_opened_pos["ExitDate"] >= next_date]

    today_s_realized_pnl = today_closed_pos["PNL"].sum()
    realized_pnl += today_s_realized_pnl

    # Giving 0 right now but we should iterate over today_s_open_pos and
    # get symbol's this day price to calculate instant profit
    today_s_unrealized_pnl = 0

    daily_profit_df.at[i, "PortfolioValue"] = realized_pnl + today_s_unrealized_pnl
