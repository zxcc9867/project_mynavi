# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import render_template, flash, request, redirect, session, url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.reservations import read_reservation
from flask_app.views.staff.common.staff_common import is_staff_login
import re


# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()
# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()


# 会員管理　list
@app.route("/staff_manage_customer", methods=["GET", "POST"])
@is_staff_login
def staff_manage_customer():
    mst_customer = read_customer()
    mst_reservation = read_reservation()

    if not mst_customer:
        flash(errorMessages.w01('会員情報'))

    # レコードの削除可否を判定
    # mst_customerに直接値を追加できないので、新しい配列を作る
    mst_customer_dict = []
    for customer in mst_customer:
        param = {'isDeletable': True,
                 'customer_id': customer.customer_id,
                 'customer_account': customer.customer_account,
                 'customer_password': customer.customer_password,
                 'customer_name': customer.customer_name,
                 'customer_zipcode': customer.customer_zipcode,
                 'customer_address': customer.customer_address,
                 'customer_phone': customer.customer_phone,
                 'customer_payment': customer.customer_payment
                 }

        for reservation in mst_reservation:
            if customer.customer_id == reservation.customer_id:
                param['isDeletable'] = False
        mst_customer_dict.append(param)

    return render_template("/staff/manage_customer/list.html", mst_customer=mst_customer_dict)


# 会員管理 input
@app.route("/staff_manage_customer/<string:mode>/input", methods=["GET", "POST"])
@is_staff_login
def input_customer(mode):
    formdata = session.get('customer_formdata', None)

    if formdata:
        customer_id = formdata['customer_id']
        customer_password = formdata['customer_password']
        customer_account = formdata['customer_account']
        customer_name = formdata['customer_name']
        customer_zipcode = formdata['customer_zipcode']
        customer_address = formdata['customer_address']
        customer_phone = formdata['customer_phone']
        customer_payment = formdata['customer_payment']
        # session削除
        session.pop('customer_formdata')

    else:
        if mode == 'update':
            customer_id = request.form['customer_id']
            customer_password = request.form['customer_password']
            customer_account = request.form['customer_account']
            customer_name = request.form['customer_name']
            customer_zipcode = request.form['customer_zipcode']
            customer_address = request.form['customer_address']
            customer_phone = request.form['customer_phone']
            customer_payment = request.form['customer_payment']

    return render_template("/staff/manage_customer/input.html",
                           customer_id=customer_id,
                           customer_name=customer_name,
                           customer_account=customer_account,
                           customer_password=customer_password,
                           customer_zipcode=customer_zipcode,
                           customer_address=customer_address,
                           customer_phone=customer_phone,
                           customer_payment=customer_payment,
                           mode=mode)


# 会員管理 confirm
@app.route("/confirm_customer/<string:mode>", methods=["POST"])
@is_staff_login
def confirm_customer(mode):
    customer_id = request.form['customer_id']
    customer_account = request.form['customer_account']
    customer_password = request.form['customer_password']
    customer_name = request.form['customer_name']
    customer_zipcode = request.form['customer_zipcode']
    customer_address = request.form['customer_address']
    customer_phone = request.form['customer_phone']
    customer_payment = request.form['customer_payment']

    isValidateError = False
    # バリデーション
    if mode == 'update':
        if len(customer_name) > 20:
            flash(errorMessages.w07('会員名', '20'))
            isValidateError = True

        if len(customer_password) < 6 or len(customer_password) > 10:
            flash(errorMessages.w08('パスワード', '6', '10'))
            isValidateError = True

        if len(customer_zipcode) != 7:
            flash(errorMessages.w06('郵便番号', '7'))
            isValidateError = True

        if re.fullmatch('[0-9]+', customer_zipcode) == None:
            flash(errorMessages.w10('郵便番号'))
            isValidateError = True

        if len(customer_address) > 50:
            flash(errorMessages.w07('住所', '50'))
            isValidateError = True

        if len(customer_phone) > 11 or len(customer_phone) < 10:
            flash(errorMessages.w08('電話番号', '10', '11'))
            isValidateError = True

        if re.fullmatch('[0-9]+', customer_phone) == None:
            flash(errorMessages.w10('電話番号'))
            isValidateError = True

    # エラーがあればセッションに情報を格納して入力画面に戻る
    if isValidateError:
        # sessionに格納
        session['customer_formdata'] = request.form
        # postにするためにcodeを指定する
        return redirect(url_for("input_customer", mode=mode), code=307)
    else:
        # エラーがなければ確認画面へ
        return render_template("/staff/manage_customer/confirm.html",
                               customer_id=customer_id,
                               customer_name=customer_name,
                               customer_account=customer_account,
                               customer_password=customer_password,
                               customer_zipcode=customer_zipcode,
                               customer_address=customer_address,
                               customer_phone=customer_phone,
                               customer_payment=customer_payment,
                               mode=mode)


# 会員管理 accept
@app.route("/accept_customer/<string:mode>", methods=["POST"])
@is_staff_login
def accept_customer(mode):
    customer_id = request.form['customer_id']

    if mode == 'update':
        update_customer(customer_id, request)
        flash(infoMessages.i02('会員'))
    if mode == 'delete':
        delete_customer(customer_id)
        flash(infoMessages.i03("会員情報"))

    return redirect("/staff_manage_customer")
