import json,sys
from database.psql_dbconn import engine
from simulator import MarketStrategySimulator
from get_positions import get_positions, create_synthetic_positions
import pandas as pd


def get_market_strategies():
    result = pd.read_sql(
        "select id from strategies s where s.id in(select ms.strategy_id from market_strategy ms)", engine)
    strategy_ids = [row["id"] for index, row in result.iterrows()]
    return strategy_ids


def add_results_to_db(strategy_id, result):
    record_count = engine.execute(f'select * from public."market_strategy_metrics:" where strategy_id={strategy_id}') \
        .rowcount

    is_exist = True if record_count == 1 else False
    if is_exist:
        engine.execute(f'update public."market_strategy_metrics:"'
                       f"set livetest_results='{json.dumps(result)}'")
    else:
        engine.execute(f'insert into public."market_strategy_metrics:" (strategy_id,livetest_results)'
                       f" values ({strategy_id},'{json.dumps(result)}')")


def get_best_ccp_for_strategy(strategy_id):
    ccp_dict = {}
    positions = get_positions(strategy_id)
    for i in range(1, 20):
        sim = MarketStrategySimulator(positions=positions, ccp=i)
        sim.simulate()
        ccp_dict[i] = round(((sim.simulated_positions["PNL"].sum() + sim.budget)
                             - sim.budget) / sim.budget * 100, 2)
    return ccp_dict


def get_daily_performance(strategy_id):
    # positions = create_synthetic_positions(1000)
    quotes = ["USDT", "BTC"]
    results = {}
    positions = get_positions(strategy_id)
    for quote in quotes:
        quote_positions = [pos for pos in positions if pos.symbol.endswith(quote)]
        ccp_results = get_best_ccp_for_strategy(strategy_id)
        best_ccp = max(ccp_results, key=ccp_results.get)
        sim = MarketStrategySimulator(positions=quote_positions, ccp=best_ccp)
        sim.simulate()
        performance_df = sim.get_daily_performance()
        performance_df_dict = dict(zip(performance_df.index, performance_df["%PV"]))
        result_ = {"quote": quote, "cc_position_count": best_ccp, "results": performance_df_dict}
        results[f"result{quote}"] = result_
    return results


def get_daily_performance_for_market_strategies():
    resp = {"success": [], "failed": []}
    market_strategies = get_market_strategies()
    for strategy_id in market_strategies:
        result = get_daily_performance(strategy_id)
        try:
            add_results_to_db(strategy_id, result)
            resp["success"].append(int(strategy_id))
        except Exception as error:
            resp["failed"].append(int(strategy_id))
            print("Error occurred while inserting to Database.", repr(error))
    return resp
