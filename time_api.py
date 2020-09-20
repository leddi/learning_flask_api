# file: time_api.py
# author: leddi
# date: 19.09.2020


from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
import os, time


app = Flask(__name__)


#SQLAlchemy config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "foobar"
app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'shortener.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#database db.model url_shortener
db = SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database created")


@app.cli.command('db_seed')
def db_seed():
    heise = Short_url(url="https://www.heise")
    golem = Short_url(url="https://www.golem.de")
    faz = Short_url(url="https://www.faz.net")

    db.session.add(heise)
    db.session.add(golem)
    db.session.add(faz)

    db.session.commit()
    print("Database seeded...")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped...")


class Short_url(db.Model):
    __tablename__ = 'short_urls'
    id = Column(Integer, primary_key=True)
    url = Column(String)   #, unique=True


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


#I can POST a URL to [project_url]/api/shorturl/new and I will receive a shortened URL in the JSON response.
#Example : {"original_url":"www.heise.de","short_url":1}
#then /api/shorturl/1 will redirect to heise.de
# dnslookup for original_url

@app.route('/api/shorturl/new', methods=['GET', 'POST'])
def new_short_url():
    if request.method == 'POST':
        original_url=request.form['url']     #form.original_url.data
        short_url=''
        newUrl = Short_url(url=original_url)
        db.session.add(newUrl)
        db.session.commit()
        return jsonify(original_url=original_url, short_url=short_url)
    else:
        return render_template('url_shortener.html')


@app.route('/api/shorturl/<int:short_url>', methods=['GET', 'POST'])
def short_url(short_url:int):
    return redirect("http://www.heise.de")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, passthrough_errors=True)