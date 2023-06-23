import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, read_customer_one, update_customer
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.models.functions.reservations import read_reservation_customer_id
from flask_app.models.functions.ticket import read_ticket_one
from flask_app.views.staff.common.staff_common import is_staff_login
from flask_app.views.customer.common.customer_common import is_customer_login
from hashlib import sha256

@app.route("/mypage", methods=['GET','POST'])
@is_customer_login
def show_mypage():
    current_customer_id = session['logged_in_customer_id']
    current_customer = read_customer_one(current_customer_id)
    current_ticket_reservations = read_reservation_customer_id(current_customer_id)
    current_reserved_event_names = []
    for current_ticket_reservation in current_ticket_reservations:
        current_ticket_id = current_ticket_reservation.ticket_id
        current_event_id = read_ticket_one(current_ticket_id).event_id
        current_reserved_event_name = read_event_one(current_event_id).event_name
        current_reserved_event_names.append(current_reserved_event_name)
        print(current_reserved_event_name)
    return render_template('/customer/mypage/mypage_top.html', current_customer=current_customer, current_ticket_reservations=current_ticket_reservations, current_reserved_event_names=current_reserved_event_names)

@app.route("/mypage/customer_info/<string:mode>", methods=['GET', 'POST'])
@is_customer_login
def show_customer_info_form(mode:str):
    """
    会員情報のフォーム
    modeによって表示する内容を若干変更する。
    残りの実装内容：無し
    """
    current_customer_id = session['logged_in_customer_id']
    customer = read_customer_one(current_customer_id)
    if mode == 'update':
        return render_template('/customer/mypage/customer_edit_form.html', customer=customer, mode=mode)
    if mode == 'delete':
        return render_template('/customer/mypage/customer_delete_form.html', customer=customer, mode=mode)


@app.route("/mypage/<string:mode>/confirm", methods=['POST'])
def show_customer_info_form_confirm(mode:str):
    """
    キャンセルボタンが押された場合は問答無用でshow_mypageに遷移する
    会員情報の確認画面を表示する。
    modeによって表示する内容を変える。
    残りの実装内容：
    ・UPD: バリデーション
    ・DEL: 無し
    """
    if request.form.get("button") == "cancel":
        return redirect(url_for('show_mypage'))
    
    if mode == 'update':
        """
        バリデーションチェックするための関数が欲しい
        """
        return "未実装:confirm/upd"
    if mode == 'delete':
        current_customer_id = request.form.get('customer_id')
        current_customer = read_customer_one(current_customer_id)
        return render_template('/customer/mypage/customer_delete_form_confirm.html', customer=current_customer, mode=mode)

@app.route("/mypage/<string:mode>/overwrite", methods=['POST'])
def customer_info_overwrite(mode:str):
    """
    キャンセルボタンが押された場合は問答無用でshow_mypageに遷移する
    渡されたmodeに応じて以下のように処理する。
    update:会員IDを受け取った情報で置き換える。パスワードだけは特殊な処理が必要。
    delete:会員IDを取得。取得した会員ID情報を基に、DBから会員情報を取得。取得した会員情報を削除する。

    懸念事項:予約が残っている状態で退会は可能か？
    残りの実装内容:
    UPD: マージ処理
    DEL: 削除処理+確認
    """
    if request.form.get("button") == "cancel":
        return redirect(url_for('show_mypage'))
    if mode=='update':
        return '未実装:overwrite/upd'
    if mode=='delete':
        return '未実装:overwrite/del'
    return ('未実装です')
    request_customer_id = request.form.get('customer_id')
    customer = read_customer_one(request_customer_id)
    if mode == 'update':
        pass
    if mode == 'delete':
        pass