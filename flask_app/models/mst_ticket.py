from flask_app.database import db
from flask_app.models.mst_event import Mst_event


class Mst_ticket(db.Model):
    __tablename__ = "mst_ticket"
    ticket_id = db.Column(db.Integer, primary_key=True,
                          autoincrement=True, unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey(Mst_event.event_id))
    ticket_seat_id = db.Column(db.String(3))
    ticket_price = db.Column(db.Integer)
    ticket_accept = db.Column(db.Integer)

    def __init__(
        self,
        ticket_id=None,
        event_id=None,
        ticket_seat_id=None,
        ticket_price=None,
        ticket_accept=None,
    ):
        self.ticket_id = ticket_id
        self.event_id = event_id
        self.ticket_seat_id = ticket_seat_id
        self.ticket_price = ticket_price
        self.ticket_accept = ticket_accept

    def __repr__(self):
        return "<Mst_ticket ticket_id:{} event_id:{} ticket_seat_id:{} ticket_price:{} ticket_accept:{}>".format(
            self.ticket_id,
            self.event_id,
            self.ticket_seat_id,
            self.ticket_price,
            self.ticket_accept,
        )
