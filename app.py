
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/flsqla"

from models import db

with app.app_context():
    db.init_app(app)
    db.create_all()
