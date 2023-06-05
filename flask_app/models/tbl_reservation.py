from flask_app.database import db
from flask_app.models.mst_ticket import Mst_ticket
from flask_app.models.mst_customer import Mst_customer


class Tbl_reservation(db.Model):
    __tablename__ = "tbl_reservation"
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Mst_ticket.ticket_id))
    customer_id = db.Column(db.Integer, db.ForeignKey(Mst_customer.customer_id))

    def __init__(
        self,
        reservation_id=None,
        ticket_id=None,
        customer_id=None,
    ):
        self.reservation_id = reservation_id
        self.ticket_id = ticket_id
        self.customer_id = customer_id

    def __repr__(self):
        return "<Tbl_reservation reservation_id:{} ticket_id:{} customer_id:{}>".format(
            self.reservation_id,
            self.ticket_id,
            self.customer_id,
        )
