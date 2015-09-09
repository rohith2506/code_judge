'''
Things done:
    1) Basic code compilation and execution done.
    2) Basic end-end framework had been built
    3) Basic sandbox and profiler

Things to do:
    1) Get output and prettify it and do them in the same page. Not only output, show errors also
    2) Automatically detect language using bayesian models

Inspirations:
https://www.codechef.com/ide
'''
import math
import requests
import os
import pdb
from processor import Processor
from flask import Flask, request, session, g, \
                  redirect, url_for, abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('show_judge.html')

@app.route('/send_data', methods=["GET", "POST"])
def send_data():
    prog_lang = request.form['prog_lang']
    code = request.form['code']
    prog_input  = request.form['prog_input']
    proc_obj = Processor()
    result = proc_obj.process(prog_lang, code, prog_input)
    return render_template('output.html', result=result)

if __name__ == "__main__":
    app.run()
