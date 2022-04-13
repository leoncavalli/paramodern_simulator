from typing import List
from models.position import Position
from database.psql_dbconn import engine
import pandas as pd
from datetime import datetime, timedelta
from random import randrange
import uuid
import random

# Get Positions from DB.


def get_positions() -> List[Position]:
    positions = []
    df = pd.read_sql(
        "select id,position_info,budget_settings,virtual,status from public.positions p where p.virtual =true "
        "order by p.created_at",
        engine)
    for index, row in df.iterrows():

        try:
            if row["status"] == "CLOSED":
                positions.append(Position(position_id=row["id"],
                                          enter_price=row["position_info"]["enterPrice"],
                                          enter_date=row["position_info"]["enterDate"],
                                          exit_price=row["position_info"]["exitPrice"],
                                          exit_date=row["position_info"]["exitDate"],
                                          exit_by=row["position_info"]["exitBy"]
                                          , profit_percent=row["position_info"]["positionPriceDiffPercent"]))
            else:
                positions.append(Position(position_id=row["id"],
                                          enter_price=row["position_info"]["enterPrice"],
                                          enter_date=row["position_info"]["enterDate"]))
        except Exception as error:
            print(row["id"], repr(error))

    return positions


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def create_synthetic_positions(position_count):
    positions = []
    from_date = datetime(2022, 1, 1)
    to_date = datetime(2022, 4, 12)
    for i in range(position_count):
        hour = random.randint(0, 60)
        enter_price = random.uniform(0.1, 10.3)
        profit_percent = random.uniform(-3.5, 4)
        exit_price = enter_price + (enter_price * profit_percent / 100)
        guid = str(uuid.uuid4())
        enter_date = random_date(from_date, to_date)
        exit_date = enter_date + timedelta(hours=hour)
        positions.append(Position(position_id=guid,
                                  enter_price=enter_price,
                                  enter_date=enter_date,
                                  exit_price=exit_price,
                                  exit_date=exit_date,
                                  exit_by=""
                                  , profit_percent=profit_percent))

    positions.sort(key=lambda x: x.enterDate)
    return positions
