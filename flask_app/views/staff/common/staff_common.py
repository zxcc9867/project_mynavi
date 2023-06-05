from functools import wraps
from flask import redirect, session, url_for
from flask_app.models.functions.staff import read_staff_one


# ログイン認証のデコレータ
def is_staff_login(view):
    @wraps(view)
    def inner(*args, **kwargs):
        # スタッフとしてログインしていない場合はスタッフログインページに遷移させる
        if not session.get('logged_in_staff') or not read_staff_one(session.get('logged_in_staff_id')):
            return redirect(url_for("staff_staff_login"))
        return view(*args, **kwargs)
    return inner
