#!/usr/bin/python3


# app-server.py
# version 1.0
# Autor: Charles Antigua
# This script generate a fake log file in this format
# {"level":"debug","ts":1578025817,"conn_id":5406983,"state":"closed","Tx":404,"Rx":879}
# the log contains an entry line per second from a specified date untill now


from flask import Response, Flask, request
from datetime import datetime, timedelta
import random
import prometheus_client
from prometheus_client import Histogram, Summary
import time

app = Flask(__name__)


_inf = float("inf")
txh = Histogram('Tx', 'Tx Histogram', buckets=(1, 500, 1000, 5000, 9000, _inf))
rxh = Histogram('Rx', 'Rx Histogram', buckets=(1, 500, 1000, 5000, 9000, _inf))
s = Summary('request_latency_seconds', 'Time Spent Generating the log')
def getRandom():
    return random.randint(1, 10000)


@app.route("/")
def hello():
    return "<h2>Welcome</h2>\
            <p><b>/generate</b> to generate the log\
            <b>/metrics</b> to see the results</p>"

@app.route("/generate")
@s.time()
def logGenerator():
    

    # Start TIme 2020 FEB 20
    t1 = datetime(2020,2,20,0,0,0)
    t2 = datetime.now()

    seconds = int((t2-t1).total_seconds())
    log_levels = ['info', 'debug', 'error', 'critical']
    states = ['open', 'closed']

    # Log File Name
    my_log = open("mylog.json", "w")

    for second in range(seconds):
        Rx = getRandom()
        Tx = getRandom()
        str_data = '{"level":"' + str(random.choice(log_levels))+ \
        '", "ts":'+ str(int((t1 + timedelta(seconds=second)).timestamp())) + \
        ', "conn_id":'+ str(second)+ ', "state":"'+  str(random.choice(states)) + \
        '", "Tx":' + str(Tx) + ', "Rx":'+ str(Rx) +'}\n'
        my_log.write(str_data)
        
        txh.observe(Tx)
        rxh.observe(Rx)

    res = []
    res.append("Logs generated")
    res.append(prometheus_client.generate_latest(s))
    res.append("go to localhost:5000/metrics to see the results")
    return Response(res, mimetype="text/plain")

@app.route("/metrics")
def requests_count():
    res = []
    res.append(prometheus_client.generate_latest(txh))
    res.append(prometheus_client.generate_latest(rxh))
    res.append(prometheus_client.generate_latest(s))
    return Response(res, mimetype="text/plain")
   

if __name__ == '__main__':
    app.run(host='localhost', debug=True)

