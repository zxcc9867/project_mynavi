import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.mst_ticket import Mst_ticket
from flask_app.models.tbl_reservation import Tbl_reservation
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.views.staff.common.staff_common import is_staff_login
from flask_app.views.customer.common.customer_common import is_customer_login

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
@is_customer_login
def show_customer_reservation(event_id): # detail.html => this_reservation.html
    event = read_event_one(event_id)
    event_category = read_event_category_one(event.event_category_id)
    ticket_id = Mst_ticket.query.with_entities(Mst_ticket.ticket_id).filter_by(event_id=event.event_id).all()
    if not ticket_id:
        return render_template('/customer/customer_ticket/ticket_reservation.html',event=event,event_category=event_category)
    else:
        current_customer_id = session['logged_in_customer_id']
        ticket_id = Mst_ticket.query.with_entities(Mst_ticket.ticket_id).filter_by(event_id=event.event_id).all()
        print(ticket_id)
        reserved_ticket = []  # 予約済みの場合のチケットidを格納するリスト
        not_reserved_ticket = []  # まだ予約していない場合のチケットidを格納するリスト
        for ticket in ticket_id:  # 一つのイベントidに紐づいているチケットidを、１つずつ取り出す
            ticket = ticket[0]  # １つのチケットidのタプルを取り出す
            # print(ticket)
            # print(Tbl_reservation.query.filter_by(customer_id=current_customer_id, ticket_id=ticket).all())
            if Tbl_reservation.query.filter_by(customer_id=current_customer_id, ticket_id=ticket).all():  # tbl_reservationで、customer_idとticket_idが一致するレコードを抽出
                reserved_ticket.append(ticket)  # ticket_idを、現在のログインしているcustomerが予約しているとreserved_ticketに格納
        # print(Tbl_reservation.query.filter_by(ticket_id='1').all())
        # print(Tbl_reservation.query.filter_by(customer_id=customer_id).all())
        # if Tbl_reservation.query.filter_by(ticket_id=ticket_id[0]).all() and Tbl_reservation.query.filter_by(customer_id=customer_id).all():
        #     flash('このイベントは予約済みです')
        #     return redirect(url_for('show_customer_event_list'))
            else:
                not_reserved_ticket.append(ticket)  # ticket_idを、現在のログインしているcustomerが予約していないとnot_reserved_ticketに格納

        
        # 予約済みかそうでないかで処理を分ける
        if len(reserved_ticket) == 0:
            return render_template('/customer/customer_ticket/ticket_reservation.html',event=event,event_category=event_category)
        else:
            flash('このイベントは予約済みです')
            return redirect(url_for('show_customer_event_list'))
                

# flash('このイベントは予約済みです')
# return redirect(url_for('show_customer_event_list'))

# flash('if Tbl_reservation.query.filter_by(customer_id=current_customer_id, ticket_id=ticket).all():のelse:')
# return render_template('/customer/customer_ticket/ticket_reservation.html',event=event,event_category=event_category )



