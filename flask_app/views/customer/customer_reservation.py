import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer ,read_customer_one
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name,convert_event_category_id
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.views.staff.common.staff_common import is_staff_login

# login処理後、detail.html から this_reservation.html へ遷移する処理
@is_staff_login # login Activate
@app.route("/customer_reservation", methods =['GET','POST']) #customer
def show_customer_reservation(event_id): # detail.html => this_reservation.html
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    return render_template('/customer/customer_event/ticket_reservation.html',event =event,event_category=event_category )

# this_reservation.html から confirm.html へ遷移する処理
@is_staff_login
def show_customer_ticket_confirm(event_id,customer_id): # detail.html => this_reservation.html
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    mydata = read_customer_one(customer_id)
    mydata_category = read_customer_one
    return render_template('/customer/customer_event/ticket_reservation.html',event =event,event_category=event_category )
