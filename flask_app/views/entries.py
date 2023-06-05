# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import render_template
from flask_app.__init__ import app


# 「/」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
def entry():
    return render_template("/index.html")

# -----------------------------------------------------------


# おまじない
if __name__ == "__main__":
    app.run(debug=True)
