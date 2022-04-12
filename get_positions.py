from typing import List
from models.position import Position
from database.psql_dbconn import engine
import pandas as pd


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

