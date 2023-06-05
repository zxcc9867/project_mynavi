from flask import Flask

from flask_app.database import init_db
import flask_app.models


def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_app.config.Config')

    init_db(app)

    return app

app = create_app()