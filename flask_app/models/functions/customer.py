from flask_app.database import db
from flask_app.models.mst_customer import Mst_customer


# 会員　新規登録
def create_customer(request):
    mst_customer = Mst_customer(
        customer_account=request.form["customer_account"],
        customer_password=request.form["customer_password"],
        customer_name=request.form["customer_name"],
        customer_payment=0,
    )
    db.session.add(mst_customer)
    db.session.commit()
    return


# 会員　登録(スクリプトから実行用)
def create_customer_script(params):
    for param in params:
        mst_customer = Mst_customer(
            customer_account=param["customer_account"],
            customer_password=param["customer_password"],
            customer_name=param["customer_name"],
            customer_zipcode=param["customer_zipcode"],
            customer_address=param["customer_address"],
            customer_phone=param["customer_phone"],
            customer_payment=param["customer_payment"],
        )
        db.session.add(mst_customer)
        db.session.commit()
    return


# 会員　一覧取得
def read_customer():
    mst_customer = Mst_customer.query.order_by(
        Mst_customer.customer_id.desc()).all()
    return mst_customer


# 会員　一件取得
def read_customer_one(customer_id):
    customer = Mst_customer.query.get(customer_id)
    return customer


# 会員アカウント名を条件に取得
def read_customer_customer_account(customer_account):
    customer = Mst_customer.query.filter(
        Mst_customer.customer_account == customer_account).all()
    return customer


# 会員　更新
def update_customer(customer_id, request):
    customer = Mst_customer.query.get(customer_id)

    customer.customer_account = request.form["customer_account"]
    customer.customer_password = request.form["customer_password"]
    customer.customer_name = request.form["customer_name"]
    customer.customer_zipcode = request.form["customer_zipcode"]
    customer.customer_address = request.form["customer_address"]
    customer.customer_phone = request.form["customer_phone"]
    customer.customer_payment = request.form["customer_payment"]

    db.session.merge(customer)
    db.session.commit()
    return


# 会員　削除
def delete_customer(customer_id):
    customer = Mst_customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return


# customer_id → customer_name変換
def convert_customer_id(customer_id):
    customer = read_customer_one(customer_id)
    if customer:
        return customer.customer_name
    else:
        return "customer does not exist"
