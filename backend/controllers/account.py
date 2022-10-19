from flask import Blueprint
from flask import request, session, jsonify
from model.user import User
from config import db
from model.crypto_currency import CryptoCurrencySchema
from model.crypto_account import CryptoAccount

account = Blueprint("account", __name__)


@account.route("/depositCrypto_Account", methods=["PATCH"])
def deposit():
    amount = request.json["amount"]
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    payment_card = user.payment_card
    crypto_account = user.crypto_account
    payment_card.money_amount -= int(amount)
    crypto_account.amount += int(amount)
    db.session.commit()


@account.route("/getCrypto")  # pregled stanja
def get_crypto():
    user_id = session.get("user_id")
    crypto_account = CryptoAccount.query.filter_by(user_id=user_id).first()
    all_crypto_currencies = crypto_account.crypto_currencies
    schema = CryptoCurrencySchema(many=True)
    results = schema.dump(all_crypto_currencies)
    return jsonify(results)


@account.route("/getMoney")  # pregled stanja
def get_money():
    user_id = session.get("user_id")
    crypto_account = CryptoAccount.query.filter_by(user_id=user_id).first()

    return jsonify({"value": crypto_account.amount}), 200


