from simulator import MarketStrategySimulator
from get_positions import get_positions, create_synthetic_positions


def get_best_ccp_for_strategy(positions):
    ccp_dict = {}
    for i in range(1, 20):
        sim = MarketStrategySimulator(positions=positions, ccp=i)
        sim.simulate()
        ccp_dict[i] = sim.simulated_positions["PNL"].sum()
    best_ccp = max(ccp_dict, key=ccp_dict.get)
    return best_ccp


def get_daily_performance():
    positions = create_synthetic_positions(1000)
    ccp = get_best_ccp_for_strategy(positions)
    sim = MarketStrategySimulator(positions=positions, ccp=ccp)
    sim.simulate()
    performance_df = sim.get_daily_performance()
    performance_df.index = performance_df["Date"]
    result = performance_df["%PortfolioValueChg"].to_json()
    return result


def get_daily_performance_with_ccp(ccp):
    positions = create_synthetic_positions(1000)
    sim = MarketStrategySimulator(positions=positions, ccp=ccp)
    sim.simulate()
    performance_df = sim.get_daily_performance()
    performance_df.index = performance_df["Date"]
    result = performance_df["%PortfolioValueChg"].to_json()
    return result

# result = get_daily_performance()
# plt.plot(result.Date, result["%PortfolioValueChg"])
