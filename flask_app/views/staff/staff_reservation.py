from operator import itemgetter
from flask import flash, render_template, request, redirect, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.event_category import read_event_category
from flask_app.models.functions.reservations import delete_reservation, param_reservation, read_reservation
from flask_app.views.staff.common.staff_common import is_staff_login


# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()
# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()


# 予約管理　list
@app.route("/staff_manage_reservation", methods=["GET", "POST"])
@is_staff_login
def staff_manage_reservation():
    tbl_reservation = read_reservation()
    reservation_param_list = sorted(param_reservation(tbl_reservation),
                                    key=itemgetter('event_date'))

    mst_event_category = read_event_category()

    # 予約情報が1件も取得できなければ、エラーメッセージ表示
    if not reservation_param_list:
        flash(errorMessages.w01('予約情報'))

    if not request.form:
        query = None
    else:
        query = int(request.form['event_category_id'])

    # セレクトボックスを動的生成
    selectbox_option = ''
    for event_category in mst_event_category:
        if query != 0 and str(query) == str(event_category.event_category_id):
            selectbox_option += '<option value=' + str(event_category.event_category_id) + \
                ' selected>' + event_category.event_category_name + '</option>'
        else:
            selectbox_option += '<option value="' + str(event_category.event_category_id) + \
                '">' + event_category.event_category_name + '</option>'

    return render_template("/staff/manage_reservation/list.html", reservation_param_list=reservation_param_list, mst_event_category=mst_event_category, query=query, selectbox_option=Markup(selectbox_option))


# 予約管理 confirm
@app.route("/confirm_reservation", methods=["POST"])
@is_staff_login
def confirm_reservation():
    reservation_detail = request.form
    return render_template("/staff/manage_reservation/confirm.html", reservation_detail=reservation_detail)


# 予約管理　accept
@app.route("/accept_reservation/<string:mode>", methods=["POST"])
@is_staff_login
def accept_reservation(mode):
    reservation_id = request.form['reservation_id']
    if mode == 'delete':
        delete_reservation(reservation_id)
        flash(infoMessages.i03('予約情報'))

    return redirect("/staff_manage_reservation")
