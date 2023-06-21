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
    events = []
    for event in events_yet:
        event_category_name = read_event_category_one(event.event_category_id)
        event_information = (event, event_category_name)
        events.append(event_information)
    return render_template('/customer/customer_event/customer_top.html', events=events)

@app.route("/customer_event/detail/<int:event_id>", methods=['GET','POST'])
def show_customer_event_detail(event_id):
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    return render_template('/customer/customer_event/detail.html', event=event, event_category=event_category)



# Matsubara追記 ==>チケット予約機能遷移設定
@app.route("/customer_event/detail/<int:event_id>/reservation", methods =['GET','POST']) #customer
def show_customer_reservation(event_id): # detail.html => this_reservation.html
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    return render_template('/customer/customer_ticket/ticket_reservation.html',event=event,event_category=event_category )



