import pandas as pd
from datetime import datetime,timedelta


class MarketStrategySimulator:
    def __init__(self, positions, ccp):
        self.closed_trades = []
        self.open_trades = []
        self.positions = positions
        self.concurrent_pos_count = ccp
        self.budget = float(10000)  # Giving initial budget
        self.budget_per_position = self.budget / self.concurrent_pos_count
        self.simulated_positions = pd.DataFrame(columns=["Id", "EnterDate", "ExitDate", "EnterPrice", "ExitPrice",
                                                         "ProfitPercent", "PositionBudget", "PNL"])

    def enter_position(self, position):
        self.open_trades.append(position)
        self.simulated_positions = self.simulated_positions.append({"Id": position.id,
                                                                    "EnterDate": position.enterDate,
                                                                    "EnterPrice": position.enterPrice,
                                                                    "PositionBudget": self.budget_per_position},
                                                                   ignore_index=True)

    def exit_position(self, position):
        self.closed_trades.append(position)
        self.open_trades.remove(position)

        profit_percent = position.profitPercent if (type(position.profitPercent) == float) else 0

        self.simulated_positions.loc[self.simulated_positions.Id == position.id, 'ExitDate'] = position.exitDate
        self.simulated_positions.loc[self.simulated_positions.Id == position.id, 'ExitPrice'] = position.exitPrice
        self.simulated_positions.loc[self.simulated_positions.Id == position.id, 'ExitDate'] = position.exitDate
        self.simulated_positions.loc[self.simulated_positions.Id == position.id, 'ProfitPercent'] = profit_percent
        self.simulated_positions.loc[self.simulated_positions.Id == position.id, 'PNL'] = (
                                                                                                  profit_percent / 100) * self.budget_per_position
        self.budget_per_position = (self.simulated_positions["PNL"].sum() + self.budget) / self.concurrent_pos_count

    def check_open_trades(self, date):
        for pos in self.open_trades:
            if pos.exitDate is not None and pos.exitDate <= date:
                self.exit_position(pos)

    def simulate(self):
        if len(self.positions) < 1:
            return "No positions found!"

        # Iterating over the positions of market strategy and simulating according to CCP count
        for i in range(len(self.positions)):
            if i == 0:
                self.enter_position(self.positions[i])
            else:
                self.check_open_trades(self.positions[i].enterDate)
                if len(self.open_trades) < self.concurrent_pos_count:
                    self.enter_position(self.positions[i])

        # Check if any closed position left
        for i in range(len(self.open_trades)):
            self.check_open_trades(datetime.utcnow())

        # If there are still open trades there should be a control to check these positions and get current prices

    def get_daily_performance(self):
        if len(self.simulated_positions)>1:
            from_date = datetime(2022, 1, 1)
            to_date = datetime(2022, 4, 12)
            date_range = pd.date_range(from_date, to_date).tolist()

            daily_profit_df = pd.DataFrame(columns=["Date", "PortfolioValue"])
            daily_profit_df.Date = date_range
            daily_profit_df.PortfolioValue = self.budget

            realized_pnl = 0
            for i in range(len(date_range)):
                next_date = date_range[i] + timedelta(days=1)

                # Get positions which are closed at this day
                today_closed_pos = self.simulated_positions[(self.simulated_positions["ExitDate"] >= date_range[i])
                                                          & (self.simulated_positions["ExitDate"] < next_date)]

                # Get positions which are still open today
                today_s_open_pos = self.simulated_positions[(self.simulated_positions["EnterDate"] < next_date) &
                                                          ((self.simulated_positions["ExitDate"] >= next_date) | (
                                                                  self.simulated_positions["ExitDate"] is None))]

                today_s_realized_pnl = today_closed_pos["PNL"].sum()
                realized_pnl += today_s_realized_pnl

                # TODO: Giving 0 right now but we should iterate over today_s_open_pos and
                # TODO: get symbol's this day price to calculate instant profit
                today_s_unrealized_pnl = 0

                daily_profit_df.at[i, "PortfolioValue"] += realized_pnl + today_s_unrealized_pnl

            daily_profit_df["%PortfolioValueChg"] = (daily_profit_df["PortfolioValue"] - self.budget) / self.budget * 100
            daily_profit_df.drop("PortfolioValue", axis=1)
            return daily_profit_df
