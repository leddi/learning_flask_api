from flask import Flask, jsonify, request
import time


# API Function:
# 
# {"unix": 1479663089000 ,"utc": "Sun, 20 Nov 2016 17:31:29 GMT"}
# on error {"error": "Invalid Date"}



app = Flask(__name__)


def seconds2utc(seconds:int):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(seconds))


@app.route('/')
def root():
    return jsonify(message="use api in form off...")


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