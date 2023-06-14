import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event
from flask_app.views.staff.common.staff_common import is_staff_login


@app.route("/show_event_list", methods=['GET','POST'])
@is_staff_login
def show_event_list():
    return render_template('/staff/manage_event/list.html')

@app.route("/staff_manage_event/detail/<int:staff_id>", methods=['GET'])
@is_staff_login
def show_event_detail(staff_id):
    staff = read_event_one(staff_id)
    return render_template('', id=staff_id)

