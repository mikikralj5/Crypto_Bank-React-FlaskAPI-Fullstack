import string
import random
from config import db, mail
from flask_mail import Message


def send_mail(user):
    letters = string.ascii_letters
    user.otp = ''.join(random.choice(letters) for i in range(5))
    db.session.commit()
    msg = Message(subject="Verification Code",
                  sender="mailzaaplikaciju21@gmail.com", recipients=[user.email])
    msg.body = "Email Verification code = " + user.otp
    try:
        mail.send(msg)
    except:
        return False

def update_crypto_currency(name, amount, crypto_currencies):
    crypto_currency = next(
        filter(lambda x: x.name == name, crypto_currencies), None)
    crypto_currency.amount += amount
    if crypto_currency.amount < 0:
        return {"error": "You don't have enough cryptocurrency"}, 400
    db.session.commit()
    return





