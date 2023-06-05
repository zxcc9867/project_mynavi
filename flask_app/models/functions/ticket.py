from flask_app.database import db
from flask_app.models.mst_ticket import Mst_ticket


# チケット　新規登録
def create_ticket(request):
    mst_ticket = Mst_ticket(
        ticket_seat_id=request.form["ticket_seat_id"],
        event_id=request.form["event_id"],
        ticket_price=request.form["ticket_price"],
        ticket_accept=request.form["ticket_accept"],
    )
    db.session.add(mst_ticket)
    db.session.commit()

    return


# チケット　一覧取得
def read_ticket():
    mst_ticket = Mst_ticket.query.order_by(
        Mst_ticket.ticket_id.desc()).all()
    return mst_ticket


# チケット　一件取得
def read_ticket_one(ticket_id):
    ticket = Mst_ticket.query.get(ticket_id)
    return ticket


# チケット　イベントIDを条件に抽出
def read_ticket_event_id(event_id):
    ticket_list = Mst_ticket.query.filter(
        Mst_ticket.event_id == event_id).all()
    return ticket_list


# チケット　更新
def update_ticket(ticket_id, request):
    ticket = Mst_ticket.query.get(ticket_id)
    ticket.event_id = request.form["event_id"]
    ticket.ticket_seat_id = request.form["ticket_seat_id"]
    ticket.ticket_price = request.form["ticket_price"]
    ticket.ticket_accept = request.form["ticket_accept"]

    db.session.merge(ticket)
    db.session.commit()

    return


# チケット　削除
def delete_ticket(ticket_id):
    ticket = Mst_ticket.query.get(ticket_id)

    db.session.delete(ticket)
    db.session.commit()

    return


# ticket_seat_id → ticket_seat_name変換
def convert_seat_id(ticket_seat_id):
    id_name_list = {
        "s00": "席種を選択",
        "s01": "特別席",
        "s02": "一般席",
        "s11": "S席",
        "s12": "A席",
        "s13": "B席",
        "s14": "C席",
        "s31": "内野席",
        "s32": "外野席"
    }
    return id_name_list[ticket_seat_id]


# 席種のselectタグに渡す値
def param_seat(selected_seat_id, defaultStatus):
    seat_id_list = ["s00", "s01", "s02", "s11",
                    "s12", "s13", "s14", "s31", "s32"]
    returnParam = []

    for index, seat_id in enumerate(seat_id_list):
        param = {"seat_id": "", "seat_name": "", "status": defaultStatus}
        param['seat_id'] = seat_id
        param['seat_name'] = convert_seat_id(param['seat_id'])

        if selected_seat_id == seat_id:
            param['status'] = "selected"

        returnParam.append(param)

    return returnParam
