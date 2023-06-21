import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, read_customer_one, update_customer
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.views.staff.common.staff_common import is_staff_login
from hashlib import sha256

@app.route("/mypage", methods=['GET','POST'])
def show_mypage():
    mypage_list = read_customer()
    user_name = session.get('username','')
    print(user_name)
    return render_template('/customer/mypage/mypage_top.html',message = mypage_list)

@app.route("/mypage/customer_info/<string:mode>", methods=['GET', 'POST'])
def show_customer_info_form(mode:str):
    """
    会員情報のフォーム
    modeによって表示する内容を若干変更する。
    """
    request_customer_id = session['logged_in_customer_id']
    customer = read_customer_one(request_customer_id)
    if mode == 'update':
        return render_template('/customer/mypage/customer_edit_form.html', customer=customer, mode=mode)
    if mode == 'delete':
        return render_template('/customer/mypage/customer_delete_form.html', customer=customer, mode=mode)


@app.route("/mypage/<string:mode>/confirm", methods=['POST'])
def show_customer_info_form_confirm(mode:str):
    """
    会員情報の確認画面を表示する。
    modeによって表示する内容を変える。
    """
    if mode == 'update':
        
        return render_template('/customer/mypage/customer_edit_form_confirm.html', customer=customer, mode=mode)
    if mode == 'delete':
        request_customer_id = request.form.get('customer_id')
        customer = read_customer_one(request_customer_id)
        return render_template('/customer/mypage/customer_delete_form_confirm.html', customer=customer, mode=mode)

@app.route("/mypage/<string:mode>/overwrite", methods=['POST'])
def customer_info_overwrite(mode:str):
    """
    渡されたmodeに応じて以下のように処理する。
    update:会員IDを受け取った情報で置き換える。パスワードだけは特殊な処理が必要。
    delete:会員IDを取得。取得した会員ID情報を基に、DBから会員情報を取得。取得した会員情報を削除する。
    """
    print(request)
    return ('未実装です')
    request_customer_id = request.form.get('customer_id')
    customer = read_customer_one(request_customer_id)
    if mode == 'update':
        pass
    if mode == 'delete':
        pass