class Position:
    def __init__(self, position_id, enter_price, enter_date, exit_date=None,
                 exit_price=None, exit_by=None, profit_percent=None):
        self.id = position_id
        self.enterPrice = enter_price
        self.enterDate = enter_date
        self.exitDate = exit_date
        self.exitPrice = exit_price
        self.exitBy = exit_by
        self.profitPercent = profit_percent




