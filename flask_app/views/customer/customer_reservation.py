import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer ,read_customer_one
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name,convert_event_category_id
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.models.functions.ticket import create_ticket
from flask_app.models.functions.reservations import create_reservation
from flask_app.views.staff.common.staff_common import is_staff_login



# this_reservation.html から confirm.html へ遷移する処理
@app.route("/customer_event/detail/<int:event_id><int:event_category_id>/reservation/comfirm" ,methods =['GET','POST'])
def show_customer_ticket_confirm(event_id, event_category_id): # this_reservation.html => confirm.html
    event = read_event_one(event_id)
    event_category = read_event_category_one(event_category_id)
    current_customer_user = read_customer_one(session['logged_in_customer_id'])
    customer_id= current_customer_user.customer_id
    customer_account = current_customer_user.customer_account
    customer_name = current_customer_user.customer_name
    customer_zipcode = current_customer_user.customer_zipcode
    customer_address = current_customer_user.customer_address
    customer_phone = current_customer_user.customer_phone

    return render_template('/customer/customer_ticket/confirm.html', event=event,event_category=event_category,customer_id=customer_id,customer_account=customer_account,customer_name=customer_name,customer_zipcode=customer_zipcode,customer_address=customer_address,customer_phone=customer_phone )

@app.route("/customer_event/detail/reservation/reserve", methods=['GET', 'POST'])
def ticket_reserve():
    ticket_id = create_ticket(request)

    create_reservation(request, ticket_id)
    flash('チケットを予約しました')
    return redirect(url_for('show_customer_event_list'))