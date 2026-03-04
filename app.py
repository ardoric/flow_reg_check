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
    tf.write(request.files['file'].read())
    tf.close()
    
    with open(tf.name, newline='', encoding='utf-16') as file:
        bad, warn, good, ignored =  flow_validator.validate(list(csv.DictReader(file, delimiter='\t')))
        return render_template('validate.html', good=good, bad=bad,warn=warn, ignored=ignored)

