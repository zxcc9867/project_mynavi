from flask_app import app
from flask import request, redirect, url_for, render_template, flash, session


@app.route('/hogehoge')
def show_entries():
    return render_template('staff/manage_event/input.html')


