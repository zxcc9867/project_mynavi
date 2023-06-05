from distutils.sysconfig import customize_compiler
from flask_app.models.functions.customer import create_customer_script, read_customer
from flask_script import Command
from flask_app import database
from flask_app.models.functions.staff import read_staff
from flask_app.models.functions.staff import create_staff_script


class InitDB(Command):
    "create database"

    def run(self):
        database.db.create_all()
        # スタッフサンプルデータの登録
        if not read_staff():

            staff_data = {
                "staff_account": "staff001",
                "staff_password": "password",
                "staff_name": "スタッフ太郎"
            }
            create_staff_script(staff_data)

        # 顧客サンプルデータの登録
        if not read_customer():
            customer_datas = [{
                "customer_account": "customer1@example.com",
                "customer_password": "password",
                "customer_name": "太客太郎",
                "customer_zipcode": "1234567",
                "customer_address": "東京都保下区三布留町1-2コーポSAMPLE101",
                "customer_phone": "00012345678",
                "customer_payment": 1,
            }, {
                "customer_account": "customer2@example.com",
                "customer_password": "password",
                "customer_name": "常連花子",
                "customer_zipcode": "1234567",
                "customer_address": "東京都保下区三布留町1-2コーポSAMPLE102",
                "customer_phone": "00012345678",
                "customer_payment": 0,
            }, {
                "customer_account": "customer3@example.com",
                "customer_password": "password",
                "customer_name": "一見一朗",
                "customer_zipcode": "1234567",
                "customer_address": "東京都保下区三布留町1-2コーポSAMPLE301",
                "customer_phone": "00012345678",
                "customer_payment": 2,
            }]
            create_customer_script(customer_datas)

        return
