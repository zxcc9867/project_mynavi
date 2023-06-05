from flask_app.database import db
from flask_app.models.mst_event_category import Mst_event_category


# イベントカテゴリ　新規登録
def create_event_category(request):
    mst_event_category = Mst_event_category(
        event_category_name=request.form["event_category_name"],
    )
    db.session.add(mst_event_category)
    db.session.commit()

    return


# イベントカテゴリ　一覧取得
def read_event_category():
    mst_event_category = Mst_event_category.query.order_by(
        Mst_event_category.event_category_id.desc()).all()
    return mst_event_category


# イベントカテゴリ　一件取得
def read_event_category_one(event_category_id):
    event_category = Mst_event_category.query.get(event_category_id)
    return event_category


# イベントカテゴリ　イベントカテゴリ名で取得
def read_event_category_category_name(event_category_name):
    event_category = Mst_event_category.query.filter(
        Mst_event_category.event_category_name == event_category_name).all()
    return event_category


# イベントカテゴリ　更新
def update_event_category(event_category_id, request):
    event_category = Mst_event_category.query.get(event_category_id)
    event_category.event_category_name = request.form["event_category_name"]

    db.session.merge(event_category)
    db.session.commit()

    return


# イベントカテゴリ　削除
def delete_event_category(event_category_id):
    event_category = Mst_event_category.query.get(event_category_id)

    db.session.delete(event_category)
    db.session.commit()

    return


# event_category_id → event_category_name
def convert_event_category_id(event_category_id):
    event_category = read_event_category_one(event_category_id)
    if event_category:
        return event_category.event_category_name
    else:
        return "error: event_category does not exist"


# event_category_name判定用
def event_category_name_judge(mst_event_category, event_category_id):
    for event_category in mst_event_category:
        if int(event_category.event_category_id) == int(event_category_id):
            return event_category.event_category_name
