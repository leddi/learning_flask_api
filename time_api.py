# file: time_api.py
# author: leddiAPI
# date: 19.09.2020
# 
# description:
# this API delivers date in JSON as follows:
# {"unix": 1479663089000 ,"utc": "Sun, 20 Nov 2016 17:31:29 GMT"}
# on error {"error": "Invalid Date"}
# expected date format:
# seconds since 1970 or date-string YYYY-MM-DD


from flask import Flask, jsonify, request
import time


app = Flask(__name__)


def seconds2utc(seconds:int):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(seconds))


@app.route('/')
def root():
    return jsonify(message="API-function: [your domain]/api/timestamp/[2020-12-12] or [seconds since 01-01-1970]")


@app.errorhandler(404)
def error_404(e):
    seconds = int(time.time())
    return jsonify(unix=seconds, utc=seconds2utc(seconds))


@app.route('/api/timestamp/<string:datum>', methods=['GET'])
def dateToTimestamp(datum:str):
    print("Datum: " + datum)
    try:
        datum = time.strptime(datum, '%Y-%m-%d')
    except ValueError:
        # expecting seconds since 1970
        if datum.isnumeric():
            seconds=int(datum)
            return jsonify(unix=seconds, utc=seconds2utc(seconds))
        else:
            return jsonify(error="Invalid Date"), 400
    seconds = int(time.mktime(datum))
    return jsonify(unix=seconds, utc=seconds2utc(seconds))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, passthrough_errors=True)