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
 reservation_time = db.Column(db.String(32))

 def __init__(self, type, field_id, event_id, reservation_time, user_id):
  super(Reservations, self).__init__(date=datetime.datetime.now(), type=type, field_id=field_id, event_id=event_id, reservation_time=reservation_time, user_id=user_id)

class ReservationSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "type", "user_id", "field_id", "reservation_time", "event_id")
        model = Reservations
reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

class Fields(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 type = db.Column(db.String(30), nullable=False)

 def __init__(self, type):
  super(Fields, self).__init__(type=type)

class Events(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 date = db.Column(db.DateTime)
 reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=True)
 seats_left = db.Column(db.Integer)

 def __init__(self, date, seats_left):
  super(Events, self).__init__(date=date, seats_left=seats_left)

@app.route('/register')
def register_page():
  return render_template('Register.html')

@app.route('/signin')
def sign_in_page():
  return render_template('Sign-In.html')

@app.route('/home')
def home_page():
  return render_template('index.html')

@app.route('/aboutus')
def about_us_page():
  return render_template('About-Us.html')

@app.route('/reservations')
def reservations_page():
  return render_template('Reservations-.html')

@app.route('/news')
def news_page():
  return render_template('News.html')

@app.route('/membership')
def membership_page():
  return render_template('Membership.html')

@app.route('/modify')
def modify_page():
  return render_template('Membership-(Members).html')

@app.route('/aboutus_si')
def aboutus_si_page():
  return render_template('About-Us_signedin.html')

@app.route('/home_si')
def home_si_page():
  return render_template('Index_signedin.html')

@app.route('/modify_si')
def modify_si_page():
  return render_template('Membership-(Members)_signedin.html')

@app.route('/reservations_si')
def reservations_si_page():
  return render_template('Reservations_signedin.html')

@app.route('/news_si')
def news_si_page():
  return render_template('News_signedin.html')


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
  resp = jsonify(token=tok)
  resp.status_code = 200
  return resp

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

    if (type=="username"):
        query.user_name = mdf
    elif (type=="first_name"):
        query.first_name = mdf
    elif (type=="last_name"):
        query.last_name = mdf
    elif (type=="email"):
        query.email = mdf
    elif (type=="phone_number"):
        query.phone_number = mdf


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
  reservation_time = request.json["reservation_time"]

  reservation = Reservations(type, field_id, event_id, reservation_time, None)
  
  token = extract_auth_token(request)
  # def __init__(self, type, field_id, event_id, reservation_time, user_id):

  if (token != None):
    try:
        userid = decode_token(token)
    except jwt.ExpiredSignatureError as error:
        abort(403)
    except jwt.InvalidTokenError as error:
        abort(403)
    reservation.user_id = userid

  print(reservation_time) #2022-04-21T21:50
  
  if (event_id != None):
    query = db.session.query(Events).filter_by(id=event_id).first()
    query.seats_left -= 1
    reservation.reservation_time = query.date

  db.session.add(reservation)
  db.session.commit()
 
  return jsonify(reservation_schema.dump(reservation))

@app.route('/reservation', methods=['GET'])
def fetch_reservations():
  token = extract_auth_token(request)

  if (token != None):
    try:
        userid = decode_token(token)
    except jwt.ExpiredSignatureError as error:
        abort(403)
    except jwt.InvalidTokenError as error:
        abort(403)

  query = db.session.query(Reservations).filter_by(user_id=userid).all()
  print(query)
  return jsonify(reservations_schema.dump(query))