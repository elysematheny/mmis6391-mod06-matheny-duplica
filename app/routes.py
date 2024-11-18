from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/regions')
def regions():
    return render_template('regions.html')


@app.route('/reports')
def reports():
    return render_template('reports.html')
