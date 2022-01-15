import React, { useState } from "react";
import httpClient from "../httpClient";
import { useNavigate } from "react-router-dom";

const Verification = () => {
  const [number, setNumber] = useState("");
  const [name, setName] = useState("");
  const [expDate, setExpDate] = useState("");
  const [securityCode, setSecurityCode] = useState("");
  const [err, setErr] = useState(false);
  const navigate = useNavigate();

  const verifyUser = async () => {
    const resp = await httpClient.patch("http://127.0.0.1:5000/verifyUser", {
      number,
      name,
      expDate,
      securityCode,
    });

    if (resp.data.verified === "true") {
      navigate("/mainPage");
    } else {
      setErr(true);
      setName("");
      setExpDate("");
      setNumber("");
      setSecurityCode("");
    }
  };

  return (
    <div className="container">
      <label style={{ fontSize: "large" }}>
        Please eneter your information to verify the account
      </label>
      <form className="add-form">
        <div className="form-control">
          <label>Card number</label>
          <input
            type="text"
            placeholder="Enter card number"
            value={number}
            onChange={(e) => {
              setNumber(e.target.value);
              setErr(false);
            }}
            required
          />
        </div>
        <div className="form-control">
          <label>Name</label>
          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-control">
          <label>Expiration date</label>
          <input
            type="text"
            placeholder="Enter your email"
            value={expDate}
            onChange={(e) => setExpDate(e.target.value)}
            required
          />
        </div>
        <div className="form-control">
          <label>CVV</label>
          <input
            type="text"
            placeholder="Enter your number"
            value={securityCode}
            onChange={(e) => setSecurityCode(e.target.value)}
            required
          />
        </div>

        <button type="button" className="btn btn-block" onClick={verifyUser}>
          Verify
        </button>
        {err ? (
          <p
            style={{
              color: "red",
              marginTop: "3rem",
              textAlign: "center",
            }}
            className="welcome"
          >
            Failed to verify, try again pls
          </p>
        ) : null}
      </form>
    </div>
  );
};

export default Verification;
