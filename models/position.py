from datetime import datetime


class Position:
    def __init__(self, position_id, symbol, enter_price, enter_date, exit_date=None,
                 exit_price=None, exit_by=None, profit_percent=None):
        self.id = position_id
        self.symbol = symbol
        self.enterPrice = enter_price
        self.enterDate = self.convert_to_datetime(enter_date)
        self.exitDate = self.convert_to_datetime(exit_date)
        self.exitPrice = exit_price
        self.exitBy = exit_by
        self.profitPercent = profit_percent

    @staticmethod
    def convert_to_datetime(date):
        if type(date) == datetime:
            return date
        else:
            try:
                return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                return None
