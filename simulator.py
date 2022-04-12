import pandas as pd
from datetime import datetime
from get_positions import get_positions


class MarketStrategySimulator:

    def __init__(self, ccp):
        self.closed_trades = []
        self.open_trades = []
        self.positions = get_positions()
        self.concurrent_pos_count = ccp
        self.budget = 10000
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
            if pos.exitDate <= date:
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
            self.check_open_trades(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"))

        # If there are still open trades there should be a control to check these positions and get current price


