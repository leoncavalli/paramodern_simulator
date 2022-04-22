from flask import Blueprint, jsonify
import manager

routes = Blueprint('routes', __name__)


@routes.route('/daily-performance/<strategy_id>', methods=['GET'])
def get_daily_performance(strategy_id):
    response = manager.get_daily_performance(strategy_id)
    return jsonify(response)


@routes.route('/daily-performance/', methods=["GET"])
def get_daily_performance_for_ms():
    response = manager.get_daily_performance_for_market_strategies()
    return jsonify(response)


@routes.route('/ccp-performance/<strategy_id>', methods=["GET"])
def get_best_ccp(strategy_id):
    response = manager.get_best_ccp_for_strategy(strategy_id)
    return jsonify(response)

