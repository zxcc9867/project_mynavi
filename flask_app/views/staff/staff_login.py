from flask import render_template, flash, request, redirect, session
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.staff import read_staff_staff_account
from flask_app.views.staff.common.staff_common import is_staff_login

# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()
# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()


# スタッフログイン
@app.route("/staff_staff_login", methods=["GET", "POST"])
def staff_staff_login():
    return render_template("/staff/staff_login.html")


# スタッフログイン処理
@app.route("/login_staff", methods=["POST"])
def login_staff():
    isLoginError = False
    staff_array = read_staff_staff_account(
        request.form["staff_account"])

    if len(staff_array) == 0:
        flash(errorMessages.w04('アカウント名'))
        isLoginError = True
    # スタッフアカウントが存在するかチェック
    else:
        staff = staff_array[0]
        # パスワードが一致するかチェック
        if request.form["staff_password"] != staff.staff_password:
            flash(errorMessages.w04('アカウント名'))
            isLoginError = True

    # エラーがあればログインページに遷移
    if isLoginError:
        return render_template("/staff/staff_login.html")

    else:
        # login処理を実行する
        session["logged_in_staff"] = True
        session["logged_in_staff_account"] = staff.staff_account
        session["logged_in_staff_id"] = staff.staff_id
        session["logged_in_staff_name"] = staff.staff_name
        flash(infoMessages.i05())
        return redirect("/staff_staff_top")


# スタッフログアウト
@app.route("/logout_staff")
@is_staff_login
def logout_staff():
    session.pop("logged_in_staff", None)
    session.pop("logged_in_staff_account", None)
    session.pop("logged_in_staff_id", None)
    session.pop("logged_in_staff_name", None)

    flash("ログアウトしました")
    return redirect("/staff_staff_login")
