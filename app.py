#!/usr/bin/env python

import urllib
import json
import os
import urllib.request

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "freebox.chaines":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("chaines")

    cost = {'1':1, '2':2, '3':3, '4':5, '5':5}

#    local_filename, headers = urllib.request.urlretrieve('http://82.66.190.153:8081/pub/remote_control?code=21357594&key=' + cost[zone])
#    html = open(local_filename)

    speech = "Les viens de vous mettre la " + zone + " (" + cost[zone] + ") ème chaîne sur votre freebox."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
