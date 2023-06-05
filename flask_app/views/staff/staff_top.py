from flask import redirect, render_template, session
from flask_app.__init__ import app
from flask_app.views.staff.common.staff_common import is_staff_login


# スタッフメニュー（トップページ）
@app.route("/staff_staff_top", methods=["GET", "POST"])
@is_staff_login
def staff_staff_top():
    if session["logged_in_staff"] == True:
        return render_template("/staff/staff_top.html")
    else:
        return redirect("/staff/staff_login.html")
