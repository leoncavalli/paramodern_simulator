import json
from flask import Flask, request, Response
import manager

app = Flask(__name__)


@app.route('/daily-performance/', methods=['GET'])
def get_daily_performance():
    response = manager.get_daily_performance()
    return json.dumps(response)


@app.route('/daily-performance-with-ccp/', methods=['POST'])
def get_daily_performance_with_ccp():
    req_data = request.json
    ccp = req_data["ccp"]
    if ccp > 50 or ccp < 1:
        return Response(status=401, response="CCP value must be between 1 and 50.")
    else:
        response = manager.get_daily_performance_with_ccp(req_data["ccp"])
        return json.dumps(response)


if __name__ == "__main__":
    app.run()
