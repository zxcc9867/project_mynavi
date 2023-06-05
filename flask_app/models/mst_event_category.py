from sqlalchemy.orm import backref
from flask_app.database import db


class Mst_event_category(db.Model):
    __tablename__ = "mst_event_category"
    event_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    event_category_name = db.Column(db.String(20))

    def __init__(
        self,
        event_category_id=None,
        event_category_name=None,
    ):
        self.event_category_id = event_category_id
        self.event_category_name = event_category_name

    # mst_eventで参照されることを宣言する
    mst_event = db.relationship("Mst_event", backref="mst_event_category")

    def __repr__(self):
        return "<Mst_event_category event_category_id:{} event_category_name:{}>".format(
            self.event_category_id,
            self.event_category_name,
        )
