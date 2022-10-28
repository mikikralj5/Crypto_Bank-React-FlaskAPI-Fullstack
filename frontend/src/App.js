import LandingPage from "./Components/LandingPage";
import RegistrationForm from "./Components/RegistrationForm";
import MainPage from "./Components/MainPage";
import CryptoGraphs from "./Components/CryptoGraphs";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ModalWindow from "./Components/ModalWindow";
import ErrorModal from "./Components/ErrorModal";
import Verification from "./Components/Verification";
import TransferValidationModal from "./Components/TransferValidationModal";
import { useState } from "react";

function App() {
  const [showModal, setShowModal] = useState(false);
  const [showErrorModal, setErrorModal] = useState(false);
  const [errorModalData, setErrorModalData] = useState("");
  const [modalTransaction, setModalTransaction] = useState(null);

  const turnOff = () => {
    setShowModal(false);
  };

  const turnOnModal = (transaction) => {
    setShowModal(true);
    setModalTransaction(transaction);
  };

  const turnOffErrorModal = () => {
    setErrorModal(false);
  };

  const turnOnErroModal = (data) => {
    setErrorModal(true);
    setErrorModalData(data);
  };

  return (
    <Router>
      <div>
        {showModal ? (
          <ModalWindow turnOff={turnOff} modalTransaction={modalTransaction} />
        ) : null}

        {showErrorModal ? (
          <ErrorModal
            turnOffErrorModal={turnOffErrorModal}
            errorModalData={errorModalData}
          />
        ) : null}

        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/mainPage"
            element={
              <MainPage
                turnOnModal={turnOnModal}
                turnOnErroModal={turnOnErroModal}
              />
            }
          />
          <Route path="/register" element={<RegistrationForm />} />
          <Route path="/verification" element={<Verification />} />
          <Route
            path="/verificationTransaction"
            element={
              <TransferValidationModal turnOnErroModal={turnOnErroModal} />
            }
          />
          <Route path="/graphs" element={<CryptoGraphs />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
