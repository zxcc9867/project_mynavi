from flask_app.database import db


class Mst_staff(db.Model):
    __tablename__ = "mst_staff"
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    staff_account = db.Column(db.String(50))
    staff_password = db.Column(db.String(10))
    staff_name = db.Column(db.String(20))

    def __init__(
        self,
        staff_id=None,
        staff_account=None,
        staff_password=None,
        staff_name=None,
    ):
        self.staff_id = staff_id
        self.staff_account = staff_account
        self.staff_password = staff_password
        self.staff_name = staff_name

    def __repr__(self):
        return "<Mst_staff staff_id:{} staff_account:{} staff_password:{} staff_name:{}>".format(
            self.staff_id,
            self.staff_account,
            self.staff_password,
            self.staff_name,
        )
