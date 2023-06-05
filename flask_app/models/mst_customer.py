from flask_app.database import db


class Mst_customer(db.Model):
    __tablename__ = "mst_customer"
    customer_id = db.Column(db.Integer, primary_key=True,
                            autoincrement=True, unique=True)
    customer_account = db.Column(db.String(50))
    customer_password = db.Column(db.String(10))
    customer_name = db.Column(db.String(20))
    customer_zipcode = db.Column(db.String(7))
    customer_address = db.Column(db.String(50))
    customer_phone = db.Column(db.String(11))
    customer_payment = db.Column(db.String(1))

    def __init__(
        self,
        customer_id=None,
        customer_account=None,
        customer_password=None,
        customer_name=None,
        customer_zipcode=None,
        customer_address=None,
        customer_phone=None,
        customer_payment=None,
    ):
        self.customer_id = customer_id
        self.customer_account = customer_account
        self.customer_password = customer_password
        self.customer_name = customer_name
        self.customer_zipcode = customer_zipcode
        self.customer_address = customer_address
        self.customer_phone = customer_phone
        self.customer_payment = customer_payment

    def __repr__(self):
        return "<Mst_customer customer_id:{} customer_account:{} customer_password:{} customer_name:{} customer_zipcode:{} customer_address:{} customer_phone:{} customer_payment:{}>".format(
            self.customer_id,
            self.customer_account,
            self.customer_password,
            self.customer_name,
            self.customer_zipcode,
            self.customer_address,
            self.customer_phone,
            self.customer_payment
        )
