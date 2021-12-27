import httpClient from "../httpClient";
import React, { useState } from "react";

const BankImport = () => {
  const [amount, setAmount] = useState(0);
  const transferMoney = async () => {
    const resp = await httpClient.patch(
      "http://127.0.0.1:5000/depositCrypto_Account",
      { amount }
    );

    console.log(resp.data);
    console.log(amount);
  };

  return (
    <div>
      <div className="operation operation--loan">
        <h2>Import money from bank account</h2>
        <form className="form form--loan">
          <input
            type="number"
            className="form__input form__input--loan-amount"
            value={amount}
            onChange={(e) => {
              setAmount(e.target.value);
            }}
          />
          <button
            type="button"
            className="form__btn form__btn--loan "
            onClick={transferMoney}
          >
            &rarr;
          </button>
          <label className="form__label form__label--loan">Amount</label>
        </form>
      </div>
    </div>
  );
};

export default BankImport;
