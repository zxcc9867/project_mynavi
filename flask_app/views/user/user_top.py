from flask import redirect, render_template, session, Markup
from flask_app.models.functions.event import read_event_with_date
from flask_app.__init__ import app

@app.route("/show_user_event_list", methods=['GET','POST'])
def show_user_event_list():
    events_yet, events_done = read_event_with_date()
    return render_template('/user/user_event/user_top.html', events_yet=events_yet, events_done=events_done)