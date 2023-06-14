# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import render_template, flash, request, redirect, session, url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, update_customer
from flask_app.models.functions.reservations import read_reservation
from flask_app.views.staff.common.staff_common import is_staff_login
import re

