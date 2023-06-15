import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event
from flask_app.views.staff.common.staff_common import is_staff_login


@app.route("/show_event_list", methods=['GET','POST'])
@is_staff_login
def show_event_list():
    events = read_event()
    return render_template('/staff/manage_event/list.html', events=events)

@app.route("/staff_manage_event/detail/<int:event_id>", methods=['GET'])
@is_staff_login
def show_event_detail(event_id):
    event = read_event_one(event_id)
    return render_template('/staff/manage_event/detail.html', event=event)

@app.route("/show_event_new", methods=['GET'])
@is_staff_login
def show_event_new():
    event_categories = read_event_category()
    return render_template('/staff/manage_event/input.html', event_categories=event_categories)

@app.route("/show_event_new/confirm", methods=['GET','POST'])
@is_staff_login
def confirm_event_new():
    event_category_id = request.form.get('event_category_id')
    event_name = request.form.get('event_name')
    event_place = request.form.get('event_place')
    event_date = request.form.get('event_date')
    event_overview = request.form.get('event_overview')
    print(event_category_id)
    return render_template('/staff/manage_event/confirm.html', event_category_id=event_category_id,event_name=event_name, event_place=event_place, event_date=event_date, event_overview=event_overview)

@app.route("/show_event_new/submit", methods=['POST'])
@is_staff_login
def submit_event_new():
    create_event(request)
    return redirect(url_for('show_event_list'))

@app.route("/show_event_edit/<int:event_id>", methods=['GET'])
@is_staff_login
def show_event_edit(event_id):
    event = read_event_one(event_id)
    return render_template('/staff/manage_event/edit.html', event=event)

@app.route("/show_event_edit/confirm", methods=['GET','POST'])
@is_staff_login
def confirm_event_edit():
    event_id = request.form.get('event_id')
    event_category_id = request.form.get('event_category_id')
    event_name = request.form.get('event_name')
    event_place = request.form.get('event_place')
    event_date = request.form.get('event_date')
    event_overview = request.form.get('event_overview')
    print(event_id)
    return render_template('/staff/manage_event/confirm_edit.html', event_id=event_id, event_category_id=event_category_id,event_name=event_name, event_place=event_place, event_date=event_date, event_overview=event_overview)

@app.route("/show_event_edit/submit", methods=['POST'])
@is_staff_login
def submit_event_edit():
    event_id = request.form.get('event_id')
    update_event(event_id, request)
    return redirect(url_for('show_event_list'))

@app.route("/delete_event_list/<int:event_id>", methods=['GET','POST'])
@is_staff_login
def delete_event_list(event_id):
    delete_event(event_id)
    return redirect(url_for('show_event_list'))