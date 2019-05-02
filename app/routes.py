from flask import render_template, request, redirect
from app import app, db
from app.models import ValveConfiguration
import datetime, random

def convert_timestamp(timestamp):
    year = int(timestamp[0:4])
    month = int(timestamp[5:7])
    day = int(timestamp[8:10])
    date = datetime.date(year, month, day)
    hour = int(timestamp[11:13])
    minute = int(timestamp[14:16])
    second = int(timestamp[17:])
    time = datetime.time(hour, minute, second)
    timestamp = datetime.datetime.combine(date, time)
    return timestamp


def convert_data(data):
    pass


@app.route('/')
def home():
    return render_template('basic_new.html')

@app.route('/configure', methods=['POST', 'GET'])
def configure():
    tmstmp = request.form['datetime']
    timestamp = convert_timestamp(tmstmp)
    exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
    if exists:
        data = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
        print(data)
        return render_template('configure.html', timestamp=tmstmp, data=data)
    if not exists:
        return render_template('configure.html', timestamp=tmstmp)

@app.route('/commit_config/<timestamp>', methods=['POST', 'GET'])
def commit_config(timestamp):
    if request.method == 'POST':
        result = request.form
        timestamp = convert_timestamp(timestamp)
        print(timestamp)
        ##############################
        fs = ['fati1', 'fati2', 'fati3', 'fati4', 'fati5', 'fati6', 'fati7', 'fati8',
              'fati9', 'fati10', 'fati11', 'fati12']
        vs = ['valve1', 'valve2', 'valve3', 'valve4', 'valve5', 'valve6', 'valve7', 'valve8']
        bs = ''
        for f in fs:
            if f in result:
                for v in vs:
                    if v in result:
                        bs = bs+'1'
                    else:
                        bs = bs+'0'
            else:
                bs = bs+'00000000'
        ##############################
        print(bs)
        exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
        if not exists:
            vc = ValveConfiguration(timestamp=timestamp, status=bs)
            db.session.add(vc)
            db.session.commit()
        print(ValveConfiguration.query.all())
    return redirect("/")