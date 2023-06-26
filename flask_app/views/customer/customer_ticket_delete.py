import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.models.functions.reservations import read_reservation_customer_id, delete_reservation

@app.route("/mypage/ticket_delete_confirm/<int:event_id>/<int:current_reservation_id>", methods=['GET','POST'])
def show_customer_ticket_delete_confirm(event_id, current_reservation_id):
    event = read_event_one(event_id)
    return render_template('/customer/mypage/customer_ticket_delete_confirm.html', event=event, current_reservation_id=current_reservation_id)

@app.route("/mypage/ticket_delete/<int:current_reservation_id>", methods=['GET','POST'])
def delete_reservation_ticket(current_reservation_id):
    delete_reservation(current_reservation_id)
    flash('チケットをキャンセルしました')
    return redirect(url_for('show_mypage'))