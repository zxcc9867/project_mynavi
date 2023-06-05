import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.event import read_event
from flask_app.models.functions.reservations import read_reservation
from flask_app.models.functions.ticket import create_ticket, delete_ticket, param_seat, read_ticket, read_ticket_event_id, update_ticket
from flask_app.views.staff.common.staff_common import is_staff_login


# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()
# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()


# イベント名のセレクトボックスに渡す値
def param_event(selected_event_id, defaultStatus):
    mst_event = read_event()
    returnParam = []

    for event in mst_event:
        param = {"event_id": "", "event_name": "", "status": defaultStatus}
        param['event_id'] = event.event_id
        param['event_name'] = event.event_name

        if selected_event_id:
            if int(selected_event_id) == int(event.event_id):
                param['status'] = "selected"
        returnParam.append(param)

    return returnParam


# チケット管理　list
@app.route("/staff_manage_ticket", methods=["GET", "POST"])
@is_staff_login
def staff_manage_ticket():
    mst_event = read_event()
    mst_reservation = read_reservation()
    seat_param_list = param_seat("", "")

    # セレクトボックスによる絞り込み
    if not request.form:
        query = "0"
    else:
        query = request.form['eventId']

    if query == "0":
        mst_ticket = read_ticket()
    else:
        mst_ticket = read_ticket_event_id(query)

    # チケット情報が1件も取得できなければ、エラーメッセージ表示
    if not mst_ticket:
        flash(errorMessages.w01('チケット'))

    # セレクトボックスを動的生成
    selectbox_option = ''
    for event in mst_event:
        if query != "0" and str(query) == str(event.event_id):
            selectbox_option += '<option value=' + str(event.event_id) + \
                ' selected>' + event.event_name + '</option>'
        else:
            selectbox_option += '<option value="' + str(event.event_id) + \
                '">' + event.event_name + '</option>'

    # レコードの削除可否を判定
    # mst_ticketに直接値を追加できないので、新しい配列を作る
    mst_ticket_dict = []
    for ticket in mst_ticket:
        param = {'isDeletable': True,
                 'ticket_id': ticket.ticket_id,
                 'event_id': ticket.event_id,
                 'ticket_seat_id': ticket.ticket_seat_id,
                 'ticket_price': ticket.ticket_price,
                 'ticket_accept': ticket.ticket_accept
                 }

        for reservation in mst_reservation:
            if ticket.ticket_id == reservation.ticket_id:
                param['isDeletable'] = False
        mst_ticket_dict.append(param)

    return render_template("/staff/manage_ticket/list.html", mst_ticket=mst_ticket_dict, mst_event=mst_event, seat_param_list=seat_param_list, selectbox_option=Markup(selectbox_option))


# チケット管理 input
@app.route("/staff_manage_ticket/<string:mode>/input", methods=["GET", "POST"])
@is_staff_login
def input_ticket(mode):
    formdata = session.get('ticket_formdata', None)

    if formdata:
        ticket_id = formdata['ticket_id']
        event_id = formdata['event_id']
        ticket_price = formdata['ticket_price']
        ticket_seat_id = formdata['ticket_seat_id']
        ticket_accept = formdata['ticket_accept']
        seat_param_list = param_seat(ticket_seat_id, "")
        event_param_list = param_event(event_id, "")
        # session削除
        session.pop('ticket_formdata')

    else:
        if mode == 'create':
            ticket_id = ''
            event_id = ''
            ticket_price = ''
            ticket_seat_id = ''
            ticket_accept = ''
            seat_param_list = param_seat("", "")
            event_param_list = param_event("", "")

        if mode == 'update':
            ticket_id = request.form.get('ticket_id')
            event_id = request.form.get('event_id')
            ticket_price = request.form.get('ticket_price')
            ticket_seat_id = request.form.get('ticket_seat_id')
            ticket_accept = request.form.get('ticket_accept')
            seat_param_list = param_seat(ticket_seat_id, "")
            event_param_list = param_event(event_id, "")

    return render_template("/staff/manage_ticket/input.html",
                           seat_param_list=seat_param_list,
                           event_param_list=event_param_list,
                           ticket_id=ticket_id,
                           ticket_price=ticket_price,
                           ticket_accept=ticket_accept,
                           mode=mode)


# チケット管理 confirm
@app.route("/confirm_ticket/<string:mode>", methods=["POST"])
@is_staff_login
def confirm_ticket(mode):
    ticket_id = request.form['ticket_id']
    event_id = request.form['event_id']
    ticket_seat_id = request.form['ticket_seat_id']
    ticket_price = request.form['ticket_price']
    ticket_accept = request.form['ticket_accept']
    seat_param_list = param_seat(ticket_seat_id, "disabled")
    event_param_list = param_event(event_id, "disabled")
    isValidateError = False

    # sessionに格納
    session['ticket_formdata'] = request.form

    # バリデーション
    if mode == 'create' or mode == 'update':
        if event_id == "0":
            flash(errorMessages.w02('イベント名'))
            isValidateError = True

        if ticket_seat_id == "s00":
            flash(errorMessages.w02('席種'))
            isValidateError = True

        if len(ticket_price) > 7:
            flash(errorMessages.w07('料金', '7'))
            isValidateError = True

        if re.fullmatch('[0-9]+', ticket_price) == None:
            flash(errorMessages.w10('料金'))
            isValidateError = True

    if isValidateError:
        # エラーがあれば入力画面に戻る
        # postにするためにcodeを指定する
        return redirect(url_for("input_ticket", mode=mode), code=307)
    else:
        # エラーがなければ確認画面に遷移
        return render_template("/staff/manage_ticket/confirm.html",
                               seat_param_list=seat_param_list,
                               event_param_list=event_param_list,
                               ticket_id=ticket_id,
                               ticket_price=ticket_price,
                               ticket_accept=ticket_accept,
                               mode=mode)


# チケット管理 accept
@app.route("/accept_ticket/<string:mode>", methods=["POST"])
@is_staff_login
def accept_ticket(mode):
    # session削除
    session.pop('ticket_formdata')

    ticket_id = request.form['ticket_id']
    if mode == 'create':
        create_ticket(request)
        flash(infoMessages.i01('チケット'))
    if mode == 'update':
        update_ticket(ticket_id, request)
        flash(infoMessages.i02('チケット'))
    if mode == 'delete':
        delete_ticket(ticket_id)
        flash(infoMessages.i03('チケット'))

    return redirect("/staff_manage_ticket")
