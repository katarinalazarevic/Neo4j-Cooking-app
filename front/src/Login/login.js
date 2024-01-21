//import "./login.css";
import { useRef, useState, useEffect, useContext } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import axios from "axios";
import React from "react";
import "./login.css";

import "../api/axios";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState(false);

  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  const handleRegisterClick = () => {
    navigate("/Register");
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const errorHandler = () => {
    setError(null);
  };

  const LoginHandler = async (event) => {
    event.preventDefault();

    const emailValue = emailRef.current.value;
    const passwordValue = passwordRef.current.value;

    setEmail(emailValue);
    setPassword(passwordValue);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/login",
        {
          email: emailValue,
          sifra: passwordValue,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response);

      if (response.status === 200) {
        if (response.data.message === "SUCCESS") {
          console.log("Poruka o uspešnoj prijavi:", response.data.message);
          localStorage.setItem("username", emailValue);
          localStorage.setItem("ime", response.data.korisnik.ime);
          localStorage.setItem("prezime", response.data.korisnik.prezime);

          return navigate("/Home");
        } else {
          console.log(
            "Neuspešna prijava! Status kod 200, ali prijava neuspešna."
          );
          window.confirm("Neuspešna prijava!");
        }
      } else {
        console.log("Neuspešna prijava! Status kod nije 200.");
        window.confirm("Neuspešna prijava!");
      }
    } catch (error) {
      console.error("Došlo je do greške prilikom prijave:", error);
      window.confirm("Neuspešna prijava!");
    }
  };

  const stampajVrednosti = (event) => {
    event.preventDefault();
    console.log("Email:", email);
    console.log("Password:", password);
  };

  return (
    <div>
      <div id="algn1">
        <div id="container">
          <p className="head">Login</p>
          <form action="/" className="input-container">
            <input
              type="email"
              placeholder="Enter email"
              className="inpt"
              value={email}
              ref={emailRef}
              onChange={handleEmailChange}
              required
            />
            <input
              type="password"
              placeholder="Enter password"
              className="inpt"
              value={password}
              ref={passwordRef}
              onChange={handlePasswordChange}
              required
            />
            <div className="rem-forgot">
              <div className="rem">
              
                
              </div>
             
            </div>
            <button type="submit" className="btn" onClick={LoginHandler}>
              Login
            </button>
          </form>
          <p className="footer">
            Don't have account?{" "}
            <a href="#" onClick={handleRegisterClick}>
              {" "}
              Register
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
