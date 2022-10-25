from flask import Blueprint
from model.user import User
from flask import jsonify, request, session, Response
from model.payment_card import PaymentCard
from model.crypto_account import CryptoAccount
from datetime import datetime, timedelta
import random
from config import db, bcrypt
from modules.modules import send_mail
from flask_jwt_extended import (
     jwt_required, create_access_token,
    get_jwt_identity, get_jwt, verify_jwt_in_request
)
from modules.authorization import admin_required

auth = Blueprint("auth", __name__)

@auth.route("/validateOTP", methods=["PATCH"])
def verification_with_otp():
    user_otp = request.json["otp"]
    email = request.json["email"]
    user = User.query.filter_by(email=email).first()

    if user_otp == user.otp:
        user.otp = "0"  # oznaka da je validiran
        db.session.commit()
        #session["user_id"] = user.id
        access_token = create_access_token(identity={"id": user.id, "role": user.role}, expires_delta=timedelta(minutes=30))
        #return jsonify(access_token=access_token), 200
        return {"token" : access_token, "verified" : "true"}
        #return {"verified": "true"}
    else:
        return {"verified": "false"}


@auth.route("/registerUser", methods=["POST"])
def register_user():
    name = request.json["name"]
    lname = request.json["lname"]
    address = request.json["address"]
    password = request.json["password"]
    email = request.json["email"]
    phone = request.json["phoneNum"]
    country = request.json["country"]
    city = request.json["city"]

    user_exists = User.query.filter_by(
        email=email).first() is not None
    if user_exists == True:
        return jsonify({"error": "User with that email already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    user = User(name, lname, address, hashed_password,
                email, phone, country, city)

    db.session.add(user)
    db.session.commit()

    create_payment_account(user)
    create_crypto_account(user)

    return Response(status=200)


@auth.route("/login", methods=["POST"])
def login_user():
    password = request.json["password"]
    email = request.json["email"]

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Unauthorized"})

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"})

    mail_status = send_mail(user)

    if mail_status:
        return Response(status=200)
    else:
        return "failed to send mail"

@auth.route("/logout", methods=["POST"])
def logout_user():

    session.pop("user_id")
    return Response(status=200)


@auth.route("/@me")
@jwt_required()
@admin_required()
def get_current_user():
    #user_id = session.get("user_id")
    user_id = get_jwt_identity()["id"]
    role = get_jwt_identity()["role"]

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({"email": user.email})

#region Functions
def gen_datetime():
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    min_year = 2023
    max_year = 2026
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def create_payment_account(user):
    card_number = str(random.randint(1000, 9999))
    cvv = str(random.randint(100, 999))
    expiration_date = gen_datetime()
    money_amount = random.randint(3000, 5000)
    payment_card = PaymentCard(card_number=card_number,
                               cvv=cvv,
                               expiration_date=expiration_date,
                               user_name=user.first_name,
                               money_amount=money_amount,
                               user=user)
    db.session.add(payment_card)
    db.session.commit()


def create_crypto_account(user):
    crypto_account = CryptoAccount(amount=0,
                                   crypto_currencies=[],
                                   user_id=user.id,
                                   user=user)
    db.session.add(crypto_account)
    db.session.commit()
    return "crypto_account created", 200
#endregion
