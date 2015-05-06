from flask import render_template, flash, redirect, url_for
from sclab_sites import app

@app.route('/indiafightasthma', methods=('GET', 'POST'))
def index():
    return render_template('ifa_index.html')
