import datetime
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request
# from flask import request
# from flask import jsonify
# from flask import abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# import jwt
from db_config import DB_CONFIG
from flask_marshmallow import Marshmallow

app = Flask(__name__)

ma = Marshmallow(app)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

CORS(app)

@app.route('/hello', methods=['GET'])
def hello_world():
    return "Hello World!"


class Customers(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 user_name = db.Column(db.String(30), unique=True)
 hashed_password = db.Column(db.String(128))
 first_name = db.Column(db.String(30), nullable=False)
 last_name  = db.Column(db.String(30), nullable=False)
 email = db.Column(db.String(30), unique=True)
 phone_number = db.Column(db.Integer, unique=True)
 is_member = db.Column(db.Boolean, default=False)

 
 def __init__(self, user_name, password, first_name, last_name, email, phone_number):
  super(Customers, self).__init__(user_name=user_name, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
  self.hashed_password = bcrypt.generate_password_hash(password)

class CustomersSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name", "first_name", "last_name", "email", "phone_number") #hashed password not returned for security purposes
        model = Customers
customers_schema = CustomersSchema()


class Staff(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 user_name = db.Column(db.String(30), unique=True)
 hashed_password = db.Column(db.String(128))
 first_name = db.Column(db.String(30), nullable=False)
 last_name  = db.Column(db.String(30), nullable=False)
 email = db.Column(db.String(30), unique=True)

 
 def __init__(self, user_name, password, first_name, last_name, email):
  super(Staff, self).__init__(user_name=user_name, first_name=first_name, last_name=last_name, email=email)
  self.hashed_password = bcrypt.generate_password_hash(password)

class Reservations(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 date = db.Column(db.DateTime)
 type = db.Column(db.Boolean, nullable=False)
 user_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True) 
 field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
 event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

 def __init__(self, type, field_id, event_id, user_id):
  super(Reservations, self).__init__(date=datetime.datetime.now(), type=type, field_id=field_id, event_id=event_id, user_id=user_id)


class Fields(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 type = db.Column(db.Boolean, nullable=False)

 def __init__(self, type):
  super(Fields, self).__init__(type=type)

class Events(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 date = db.Column(db.DateTime)
 reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=True)

 def __init__(self, type):
  super(Events, self).__init__(type=type)

@app.route('/customer', methods=['POST'])
def create_user():
 unm = request.json["user_name"]
 pwd_unhashed = request.json["password"]
 first_name = request.json["first_name"]
 last_name = request.json["last_name"]
 email = request.json["email"]
 phone_number = request.json["phone_number"]
 is_member = False

 customer = Customers(unm, pwd_unhashed, first_name, last_name, email, phone_number)

 db.session.add(customer)
 db.session.commit()
 
 return jsonify(customers_schema.dump(customer))