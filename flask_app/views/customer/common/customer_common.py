from functools import wraps
from flask import redirect, session, url_for
from flask_app.models.functions.customer import read_customer_one


# ログイン認証のデコレータ
def is_customer_login(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # ユーザーとしてログインしていない場合はユーザーログインページに遷移させる
        if not session.get('logged_in_customer') or not read_customer_one(session.get('logged_in_customer_id')):
            return redirect(url_for("show_login"))
        return view(*args, **kwargs)
    return inner
