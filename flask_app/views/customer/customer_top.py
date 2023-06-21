import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.views.staff.common.staff_common import is_staff_login

@app.route("/show_customer_event_list", methods=['GET','POST'])
def show_customer_event_list():
    events_yet, events_done = read_event_with_date()
    return render_template('/customer/customer_event/customer_top.html', events_yet=events_yet, events_done=events_done)

@app.route("/customer_event/detail/<int:event_id>", methods=['GET','POST'])
def show_customer_event_detail(event_id):
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    return render_template('/customer/customer_event/detail.html', event=event, event_category=event_category)

@app.route("/mypage", methods=['GET','POST'])
def show_mypage():
    mypage_list = read_customer()
    user_name = session.get('username','')
    print(user_name)
    return render_template('/customer/mypage/mypage_top.html',message = mypage_list)