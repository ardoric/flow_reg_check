from flask import Flask
from flask import render_template
from flask import request

import flow_validator
import csv
import codecs
import tempfile

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.post("/validate")
def validate():
    tf = tempfile.NamedTemporaryFile(delete_on_close=False)
    request.files['file'].save(tf)
    tf.close()
    
    bad, warn, good, ignored =  flow_validator.validate(flow_validator.parse_flow(tf.name))
    return render_template('validate.html', good=good, bad=bad,warn=warn, ignored=ignored)

