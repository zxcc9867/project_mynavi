from flask_app.database import db
from flask_app.models.mst_staff import Mst_staff


# スタッフ　新規登録（スクリプトから実行用）
def create_staff_script(param):
    mst_staff = Mst_staff(
        staff_account=param["staff_account"],
        staff_password=param["staff_password"],
        staff_name=param["staff_name"],
    )
    db.session.add(mst_staff)
    db.session.commit()
    return


# スタッフ　一覧取得
def read_staff():
    mst_staff = Mst_staff.query.order_by(
        Mst_staff.staff_id.desc()).all()
    return mst_staff


# スタッフ　一件取得
def read_staff_one(staff_id):
    staff = Mst_staff.query.get(staff_id)
    return staff


# スタッフアカウント名を条件に取得
def read_staff_staff_account(staff_account):
    staff = Mst_staff.query.filter(
        Mst_staff.staff_account == staff_account).all()
    return staff


# スタッフ　更新
def update_staff(staff_id, request):
    staff = Mst_staff.query.get(staff_id)

    staff_account = request['form']["staff_account"]
    staff_password = request['form']["staff_password"]
    staff_name = request['form']["staff_name"]

    db.session.merge(staff)
    db.session.commit()

    return


# スタッフ　削除
def delete_staff(staff_id):
    staff = Mst_staff.query.get(staff_id)

    db.session.delete(staff)
    db.session.commit()
    return
