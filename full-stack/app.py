from argparse import RawDescriptionHelpFormatter
from dataclasses import field
import datetime
import json
import os
import pwd
from time import sleep
import webbrowser
from flask_bcrypt import Bcrypt
from flask import Flask, abort, jsonify, redirect, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
from db_config import DB_CONFIG
from flask_marshmallow import Marshmallow
from flask import render_template
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

app = Flask(__name__)

ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONFIG
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

CORS(app)

if __name__ == "__main__":
    app.run()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "sportsys.430@gmail.com"
app.config["MAIL_PASSWORD"] = "430group_2"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
s = URLSafeTimedSerializer("Thisisasecret!")

dict = {}


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    is_member = db.Column(db.Boolean, default=False)

    def __init__(self, user_name, password, first_name, last_name, email, phone_number):
        super(Customers, self).__init__(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )
        self.hashed_password = bcrypt.generate_password_hash(password)


class CustomersSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "user_name",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        )  # hashed password not returned for security purposes
        model = Customers


customers_schema = CustomersSchema()


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True)

    def __init__(self, user_name, password, first_name, last_name, email):
        super(Staff, self).__init__(
            user_name=user_name, first_name=first_name, last_name=last_name, email=email
        )
        self.hashed_password = bcrypt.generate_password_hash(password)


class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    type = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), nullable=True
    )  # user id null if event
    field_id = db.Column(db.Integer, db.ForeignKey("fields.id"), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=True)
    reservation_time = db.Column(db.String(32))

    def __init__(self, type, field_id, event_id, reservation_time, user_id):
        super(Reservations, self).__init__(
            date=datetime.datetime.now(),
            type=type,
            field_id=field_id,
            event_id=event_id,
            reservation_time=reservation_time,
            user_id=user_id,
        )


class ReservationSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "date",
            "type",
            "user_id",
            "field_id",
            "reservation_time",
            "event_id",
        )
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
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservations.id"), nullable=True
    )
    seats_left = db.Column(db.Integer)

    def __init__(self, date, seats_left):
        super(Events, self).__init__(date=date, seats_left=seats_left)


@app.route("/register")
def register_page():
    return render_template("Register.html")


@app.route("/signin")
def sign_in_page():
    return render_template("Sign-In.html")


@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/aboutus")
def about_us_page():
    return render_template("About-Us.html")


@app.route("/reservations")
def reservations_page():
    return render_template("Reservations-.html")


@app.route("/news")
def news_page():
    return render_template("News.html")


@app.route("/membership")
def membership_page():
    return render_template("Membership.html")


@app.route("/modify")
def modify_page():
    return render_template("Membership-(Members).html")


@app.route("/aboutus_si")
def aboutus_si_page():
    return render_template("About-Us_signedin.html")


@app.route("/home_si")
def home_si_page():
    return render_template("Index_signedin.html")


@app.route("/modify_si")
def modify_si_page():
    return render_template("Membership-(Members)_signedin.html")


@app.route("/reservations_si")
def reservations_si_page():
    return render_template("Reservations_signedin.html")


@app.route("/news_si")
def news_si_page():
    return render_template("News_signedin.html")


@app.route("/showroom")
def showroom_page():
    return render_template("Showroom.html")


@app.route("/showroom_si")
def showroom_si_page():
    return render_template("Showroom_signedin.html")


@app.route("/confirmation")
def confirm():
    return render_template("confirmation.html")

@app.route('/forgot_password')
def forgot_password2_page():
  return render_template('Forgot_password2.html')




@app.route("/table2")
def table2():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "templates/webbrowser.html")
    file = open(filename, "r")
    return file.read()


@app.route("/customer", methods=["POST"])
def create_user():
    unm = request.json["user_name"]
    pwd_unhashed = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    phone_number = request.json["phone_number"]

    token = s.dumps(email, salt="email-confirm")
    msg = Message("Confirm Email", sender="sportsys.430@gmail.com", recipients=[email])
    link = url_for("confirm_email", token=token, _external=True)
    msg.body = "Your link to confirm your account is {}".format(link)
    mail.send(msg)

    dict[token] = False

    helper(token, unm, pwd_unhashed, first_name, last_name, email, phone_number)

    customer = Customers(unm, pwd_unhashed, first_name, last_name, email, phone_number)

    return jsonify(customers_schema.dump(customer))


def helper(token, unm, pwd_unhashed, first_name, last_name, email, phone_number):
    while dict[token] != True:
        None

    customer = Customers(unm, pwd_unhashed, first_name, last_name, email, phone_number)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customers_schema.dump(customer))


@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = s.loads(token, salt="email-confirm", max_age=3600)
    except SignatureExpired:
        return "<h1>The token is expired!</h1>"

    dict[token] = True
    return "<h1>Account confirmed</h1>"


@app.route("/signin", methods=["POST"])
def auth():
    unm = request.json["user_name"]
    pwd_unhashed = request.json["password"]

    if unm == "" or pwd_unhashed == "":
        abort(400)

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if query == None:
        abort(403)

    if bcrypt.check_password_hash(query.hashed_password, pwd_unhashed) == False:
        abort(403)

    tok = create_token(query.id)
    resp = jsonify(token=tok)
    resp.status_code = 200
    return resp


def create_token(user_id):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=4),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get("Authorization")
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, "HS256")
    return payload["sub"]


@app.route("/reset_password", methods=["POST"])
def reset_password():
    unm = request.json["user_name"]
    old_pwd_unhashed = request.json["old_password"]
    new_pwd1 = request.json["new_password1"]
    new_pwd2 = request.json["new_password2"]

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if new_pwd1 != new_pwd2:
        abort(403)
    if bcrypt.check_password_hash(query.hashed_password, old_pwd_unhashed) == False:
        abort(403)

    query.hashed_password = bcrypt.generate_password_hash(new_pwd1)
    db.session.commit()
    return jsonify("Password has been changed")


@app.route("/modify_customer", methods=["POST"])
def modify_customer():
    unm = request.json["user_name"]
    pwd = request.json["password"]
    type = request.json["type"]
    mdf = request.json["modification"]

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if unm == "" or pwd == "":
        abort(400)

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if query == None:
        abort(403)

    if bcrypt.check_password_hash(query.hashed_password, pwd) == False:
        abort(403)

    if type == "username":
        query.user_name = mdf
    elif type == "first_name":
        query.first_name = mdf
    elif type == "last_name":
        query.last_name = mdf
    elif type == "email":
        query.email = mdf
    elif type == "phone_number":
        query.phone_number = mdf

    db.session.commit()
    return jsonify("Modification Successful")


@app.route("/delete_customer", methods=["POST"])
def delete_customer():
    unm = request.json["user_name"]
    pwd_unhashed = request.json["password"]
    confirmation = request.json["confirmation"]

    query = db.session.query(Customers).filter_by(user_name=unm).first()

    if query == None:
        abort(403)

    if bcrypt.check_password_hash(query.hashed_password, pwd_unhashed) == False:
        abort(403)

    if confirmation != pwd_unhashed:
        abort(403)

    db.session.query(Customers).filter_by(user_name=unm).delete()
    db.session.commit()
    return jsonify("Deletion successful")


@app.route("/reservation", methods=["POST"])
def create_reservation():
    type = request.json["type"]
    field_id = request.json["field_id"]
    event_id = request.json["event_id"]
    reservation_time = request.json["reservation_time"]

    reservation = Reservations(type, field_id, event_id, reservation_time, None)

    token = extract_auth_token(request)

    if token != None:
        try:
            userid = decode_token(token)
        except jwt.ExpiredSignatureError as error:
            abort(403)
        except jwt.InvalidTokenError as error:
            abort(403)
        reservation.user_id = userid

    query = (
        db.session.query(Reservations)
        .filter_by(reservation_time=reservation_time, field_id=field_id)
        .first()
    )
    print(query)
    if query != None:
        abort(403)

    if event_id != None:
        query = db.session.query(Events).filter_by(id=event_id).first()
        if query.seats_left == 0:
            abort(403)
        query.seats_left -= 1
        reservation.reservation_time = query.date

    db.session.add(reservation)
    db.session.commit()

    return jsonify(reservation_schema.dump(reservation))


@app.route("/getUserInfo", methods=["GET"])
def getUserInfo():
    token = extract_auth_token(request)
    userid = decode_token(token)
    query = db.session.query(Customers).filter_by(id=userid).first()
    return jsonify(customers_schema.dump(query))


@app.route("/table", methods=["GET"])
def table():
    token = extract_auth_token(request)
    userid = decode_token(token)
    result = db.session.query(Reservations).filter_by(user_id=userid).all()
    print("_----------")
    print(result)

    p = []

    result = reservations_schema.dump(result)

    # for x in result:
    #   print (x)
    for row in result:
        row["field_id"] = str(row["field_id"]).replace("1", "Basketball")
        row["field_id"] = str(row["field_id"]).replace("2", "Tennis")
        row["field_id"] = str(row["field_id"]).replace("3", "Boxing")
        row["field_id"] = str(row["field_id"]).replace("4", "Volleyball")
        row["field_id"] = str(row["field_id"]).replace("5", "Football")
        row["field_id"] = str(row["field_id"]).replace("None", "")
        row["event_id"] = str(row["event_id"]).replace("0", "By the pool with Sax")
        row["event_id"] = str(row["event_id"]).replace(
            "1", "Mega vs speed (Football game)"
        )
        row["event_id"] = str(row["event_id"]).replace("2", "Basketball workshop")
        row["event_id"] = str(row["event_id"]).replace(
            "3", "Zinedine zidane freestyle show"
        )
        row["event_id"] = str(row["event_id"]).replace(
            "4", "Mohammad Ali vs David Abboud (boxing match)"
        )
        row["event_id"] = str(row["event_id"]).replace("None", "")

    print(result)

    tbl = "<tr><td>Reservation-Time</td><td>Field</td><td>Event</td><td>Reservation-ID</td></tr>"
    p.append(tbl)

    for row in result:
        a = "<tr><td>%s</td>" % row["reservation_time"]
        print("----------------------------------")
        print(a)
        p.append(a)
        b = "<td>%s</td>" % row["field_id"]
        p.append(b)
        c = "<td>%s</td>" % row["event_id"]
        p.append(c)
        d = "<td>%s</td>" % row["id"]
        p.append(d)

    contents = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
  <html>
  <head>
  <script>
    window.onload=function(){
    console.log("script loaded")
    var mod_button = document.getElementById("delete_id_button");
    mod_button.addEventListener("click", del_res_func);
}

var SERVER_URL = "http://127.0.0.1:5000"

async function del_res_func(){
    console.log("Func");
    var id = document.getElementById("reservation_id").value;

        const data = {  "id":id,
                        };
                        

        const response = await fetch(`${SERVER_URL}/delete_reservation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
    })
    if (response.ok) {
        window.alert("Reservation cancelled.");
        window.open("http://127.0.0.1:5000/reservations_si","_self");
    }
    else {
        console.log("error");
    }

}
  </script>
  <meta content="text/html; charset=ISO-8859-1"
  http-equiv="content-type">
  <title>Your Reservations</title>
  </head>
  <body>
  <table>
  %s
  </table>
  </body>
  <center><input type="number" pattern="\+?\d{0,3}[\s\(\-]?([0-9]{2,3})[\s\)\-]?([\s\-]?)([0-9]{3})[\s\-]?([0-9]{2})[\s\-]?([0-9]{2})" placeholder="Reservation ID" id="reservation_id" name="reservation" required=""></center>
  <center><button type="button" id="delete_id_button">Cancel Reservation</button></center>
  </html>
  """ % (
        p
    )

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "templates/webbrowser.html")

    output = open(filename, "w")
    output.write(contents)
    output.close()

    return jsonify(filename)

@app.route("/forgot_password", methods=["POST"])
def forgot():
    email = request.json["email"]

    token = s.dumps(email, salt="password-reset")
    msg = Message("Reset Password", sender="sportsys.430@gmail.com", recipients=[email])
    link = url_for("forgot_password_reset", token=token, _external=True)
    msg.body = "Your link to reset your password is {}".format(link)
    mail.send(msg)

    return jsonify(email)


@app.route("/forgot_password_reset/<token>", methods=["POST"])
def forgot2(token):
    try:
        email = s.loads(token, salt="password-reset", max_age=3600)
    except SignatureExpired:
        return "<h1>The token is expired!</h1>"
    
    if token != None:
        try:
            userid = decode_token(token)
        except jwt.ExpiredSignatureError as error:
            abort(403)
        except jwt.InvalidTokenError as error:
            abort(403)
    
    pwd = request.json["new_password"]
    pwd_conf = request.json["confirm_new_password"]

    query = db.session.query(Customers).filter_by(id=userid).first()
    
    if pwd != pwd_conf:
        abort(403)

    query.hashed_password = bcrypt.generate_password_hash(pwd)
    db.session.commit()

    dict[token] = True

    return "<h1>Password Changed</h1>"

@app.route("/delete_reservation", methods=["POST"])
def delete_reservation():
    id = request.json["id"]

    query = db.session.query(Reservations).filter_by(id=id).first()

    if query == None:
        abort(403)

    db.session.query(Reservations).filter_by(id=id).delete()
    db.session.commit()
    return jsonify("Deletion successful")
    
    