from flask_app.database import db
from flask_app.models.mst_event_category import Mst_event_category


class Mst_event(db.Model):
    __tablename__ = "mst_event"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    event_category_id = db.Column(db.Integer, db.ForeignKey(Mst_event_category.event_category_id))
    event_name = db.Column(db.String(50))
    event_date = db.Column(db.String(10))
    event_place = db.Column(db.String(30))
    event_overview = db.Column(db.String(200))

    def __init__(
        self,
        event_id=None,
        event_category_id=None,
        event_name=None,
        event_date=None,
        event_place=None,
        event_overview=None,
    ):
        self.event_id = event_id
        self.event_category_id = event_category_id
        self.event_name = event_name
        self.event_date =  event_date
        self.event_place = event_place
        self.event_overview = event_overview

    def __repr__(self):
        return "<Mst_event event_id:{} event_category_id:{} event_name:{} event_date:{} event_place:{} event_overview:{}>".format(
            self.event_id,
            self.event_category_id,
            self.event_name,
            self.event_date,
            self.event_place,
            self.event_overview,
        )
