# file: time_api.py
# author: leddi
# date: 19.09.2020


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


#{"ipaddress":"159.20.14.100","language":"en-US,en;q=0.5",
#"software":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"}
@app.route('/api/whoami')
def whoami():
    ip = request.remote_addr
    useragent = str(request.user_agent)
    language = str(request.accept_languages)
    print(language)
    return jsonify(ipaddress=ip, language=language, software=useragent)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, passthrough_errors=True)