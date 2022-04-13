from argparse import RawDescriptionHelpFormatter
import datetime
from flask_bcrypt import Bcrypt
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import jwt
from db_config import DB_CONFIG
from flask_marshmallow import Marshmallow
from flask import render_template

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

app = Flask(__name__)

ma = Marshmallow(app)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

CORS(app)

@app.route('/hello')
def hello_world():
  return render_template('register.html')

if __name__ == '__main__':
   app.run()


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
 user_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True) #user id null if event
 field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=True)
 event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)

 def __init__(self, type, field_id, event_id, user_id):
  super(Reservations, self).__init__(date=datetime.datetime.now(), type=type, field_id=field_id, event_id=event_id, user_id=user_id)

class ReservationSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "type", "user_id", "field_id", "event_id")
        model = Reservations
reservations_schema = ReservationSchema()

class Fields(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 type = db.Column(db.String(30), nullable=False)

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
 

@app.route('/signin', methods=['POST'])
def auth():
  unm = request.json["user_name"]
  pwd_unhashed = request.json["password"]

  if(unm == "" or pwd_unhashed == ""):
    abort(400)

  query = db.session.query(Customers).filter_by(user_name = unm).first()
  
  if (query == None):
    abort(403)

  if (bcrypt.check_password_hash(query.hashed_password, pwd_unhashed) == False):
    abort(403)

  tok = create_token(query.id)
  return jsonify(token=tok)

def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
)
def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
      return auth_header.split(" ")[1]
    else:
      return None

def decode_token(token):
  payload = jwt.decode(token, SECRET_KEY, 'HS256')
  return payload['sub']

@app.route('/reset_password', methods=['POST'])
def reset_password():
    unm = request.json["user_name"]
    old_pwd_unhashed = request.json["old_password"]
    new_pwd1 = request.json["new_password1"]
    new_pwd2 = request.json["new_password2"]

    query = db.session.query(Customers).filter_by(user_name = unm).first()

    if (new_pwd1 != new_pwd2):
        abort(403)
    if (bcrypt.check_password_hash(query.hashed_password, old_pwd_unhashed) == False):
        abort(403)

    query.hashed_password = bcrypt.generate_password_hash(new_pwd1)
    db.session.commit()
    return jsonify("Password has been changed")

@app.route('/modify_customer', methods=['POST'])
def modify_customer():
    unm = request.json["user_name"]
    pwd = request.json["password"]
    type = request.json["type"]
    mdf = request.json["modification"]

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if (unm == "" or pwd == ""):
        abort(400)

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if (query == None):
        abort(403)

    if (bcrypt.check_password_hash(query.hashed_password, pwd) == False):
        abort(403)

    if (type=="user_name"):
        query.user_name = mdf
    elif (type=="first_name"):
        query.first_mame = mdf
    elif (type=="last_name"):
        query.last_mame = mdf
    elif (type=="email"):
        query.email = mdf
    elif (type=="phone_number"):
        query.phone_number = mdf
    else:
        abort(403)

    db.session.commit()
    return jsonify("Modification Successful")

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    unm = request.json["user_name"]
    pwd_unhashed = request.json["password"]
    confirmation = request.json["confirmation"]

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if (query == None):
        abort(403)

    if (bcrypt.check_password_hash(query.hashed_password, pwd_unhashed) == False):
        abort(403)

    if (confirmation!=True):
        abort(403)

    db.session.query(Customers).filter_by(user_name=unm).delete()
    db.session.commit()
    return jsonify("Deletion successful")


@app.route('/reservation', methods=['POST'])
def create_reservation():
  type = request.json["type"]
  field_id = request.json["field_id"]
  event_id = request.json["event_id"]

  reservation = Reservations(type, field_id, event_id, None)
  
  token = extract_auth_token(request)
  # def __init__(self, type, field_id, event_id, user_id):

  if (token != None):
    try:
        userid = decode_token(token)
    except jwt.ExpiredSignatureError as error:
        abort(403)
    except jwt.InvalidTokenError as error:
        abort(403)
    reservation.user_id = userid
    
  db.session.add(reservation)
  db.session.commit()
 
  return jsonify(reservations_schema.dump(reservation))