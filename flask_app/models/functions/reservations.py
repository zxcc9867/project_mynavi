from flask_app.database import db
from flask_app.models.tbl_reservation import Tbl_reservation
from flask_app.models.functions.customer import convert_customer_id
from flask_app.models.functions.event import read_event_one
from flask_app.models.functions.event_category import convert_event_category_id
from flask_app.models.functions.ticket import convert_seat_id, read_ticket_one


# 予約　新規登録
def create_reservation(request):
    tbl_reservation = Tbl_reservation(
        customer_id=request.form["customer_id"],
        ticket_id=request.form["ticket_id"],
    )

    db.session.add(tbl_reservation)
    db.session.commit()

    return


# 予約　一覧取得
def read_reservation():
    tbl_reservation = Tbl_reservation.query.order_by(
        Tbl_reservation.reservation_id.desc()).all()
    return tbl_reservation


# 予約　一件取得
def read_reservation_one(reservation_id):
    reservation = Tbl_reservation.query.get(reservation_id)
    return reservation


# 予約　会員IDを条件に抽出
def read_reservation_customer_id(customer_id):
    reservation_list = Tbl_reservation.query.filter(
        Tbl_reservation.customer_id == customer_id).all()
    return reservation_list


# 予約　削除
def delete_reservation(reservation_id):
    reservation = Tbl_reservation.query.get(reservation_id)

    db.session.delete(reservation)
    db.session.commit()
    return


# 予約情報のparamを返す
def param_reservation(reservation_list):
    reservation_param_list = []

    for reservation in reservation_list:
        param = {
            "reservation_id": "",
            "event_id": "",
            "event_name": "",
            "event_category_id": "",
            "event_category_name": "",
            "event_date": "",
            "event_place": "",
            "event_overview": "",
            "ticket_seat_name": "",
            "ticket_price": "",
            "customer_name": ""
        }

        param['reservation_id'] = reservation.reservation_id
        ticket = read_ticket_one(reservation.ticket_id)
        param['ticket_price'] = ticket.ticket_price
        param['ticket_seat_name'] = convert_seat_id(ticket.ticket_seat_id)
        event = read_event_one(ticket.event_id)
        param['event_date'] = event.event_date
        param['event_id'] = event.event_id
        param['event_name'] = event.event_name
        param['customer_name'] = convert_customer_id(reservation.customer_id)
        param['event_category_id'] = event.event_category_id
        param['event_category_name'] = convert_event_category_id(
            event.event_category_id)
        param['event_place'] = event.event_place
        param['event_overview'] = event.event_overview

        reservation_param_list.append(param)

    return reservation_param_list
