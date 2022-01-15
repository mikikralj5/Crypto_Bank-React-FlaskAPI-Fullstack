import React from "react";
import TransactionRequest from "./TransactionRequest";

const TransactionRequestLits = ({
  userTransactionReqeusts,
  turnOnModal,
  onRequestResolve,
  updateTransactions,
}) => {
  return (
    <div>
      {userTransactionReqeusts.map((transactionRequest, index) => (
        <TransactionRequest
          transactionRequest={transactionRequest}
          key={index}
          turnOnModal={turnOnModal}
          onRequestResolve={onRequestResolve}
          updateTransactions={updateTransactions}
        />
      ))}
    </div>
  );
};

export default TransactionRequestLits;
