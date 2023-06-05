from flask_app.database import db
from flask_app.models.mst_event import Mst_event


# イベント　新規登録
def create_event(request):
    mst_event = Mst_event(
        event_name=request.form["event_name"],
        event_category_id=request.form["event_category_id"],
        event_date=request.form["event_date"],
        event_place=request.form["event_place"],
        event_overview=request.form["event_overview"],
    )
    db.session.add(mst_event)
    db.session.commit()

    return


# イベント　一覧取得
def read_event():
    mst_event = Mst_event.query.order_by(
        Mst_event.event_id.desc()).all()
    return mst_event


# イベント　一件取得
def read_event_one(event_id):
    event = Mst_event.query.get(event_id)
    return event


# イベント　イベントカテゴリIDを条件に取得
def read_event_event_category(event_category_id):
    event = Mst_event.query.filter(
        Mst_event.event_category_id == event_category_id).all()
    return event


# イベントカテゴリ　イベント名で取得
def read_event_event_name(event_name):
    event = Mst_event.query.filter(
        Mst_event.event_name == event_name).all()
    return event


# イベント　更新
def update_event(event_id, request):
    event = Mst_event.query.get(event_id)

    event.event_name = request.form["event_name"]
    event.event_category_id = request.form["event_category_id"]
    event.event_date = request.form["event_date"]
    event.event_place = request.form["event_place"]
    event.event_overview = request.form["event_overview"]

    db.session.merge(event)
    db.session.commit()

    return


# イベント　削除
def delete_event(event_id):
    event = Mst_event.query.get(event_id)

    db.session.delete(event)
    db.session.commit()

    return
