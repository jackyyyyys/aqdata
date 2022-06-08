from flask import Flask
from test_use_model import quality

app = Flask(__name__)

@app.route("/quality/<params>")

def index(params):
    paramf = [float(p) for p in params.split(',')]
    prediction = quality(*paramf)
    return str(prediction)

"""
RUN
set FLASK_APP=flask_serve
py -m flask run
"""