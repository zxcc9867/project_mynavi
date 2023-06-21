import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer ,read_customer_one
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name,convert_event_category_id
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.views.staff.common.staff_common import is_staff_login



# this_reservation.html から confirm.html へ遷移する処理
@is_staff_login
@app.route("/show_customer_ticket_confirm" ,methods =['POST'])
def show_customer_ticket_confirm(event_id): # this_reservation.html => confirm.html
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    customer_account = request.form.get('customer_account')
    customer_password = request.form['customer_password']
    customer_name = request.form.get('customer_name')
    customer_zipcode = request.form.get('customer_zipcode')
    customer_address = request.form.get('customer_address')
    customer_phone = request.form.get('customer_phone')
    customer_payment = request.form.get('customer_payment')
    return render_template('/customer/customer_event/confirm.html',event =event,event_category=event_category,customer_account=customer_account,customer_password=customer_password,customer_name=customer_name,customer_zipcode=customer_zipcode,customer_address=customer_address,customer_phone=customer_phone )
