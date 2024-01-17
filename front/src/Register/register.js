import { Navigate, useNavigate } from 'react-router-dom';
import  './register.css'
import { useState } from 'react';
import axios from 'axios';
const  Register = () =>
{

  const navigate = useNavigate();
  const [ime, setIme] = useState("");
  const [prezime, setprezime] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [datum,setDatum]= useState("");
//   const [grad, setGrad] = useState("");
//   const [ulica, setulica] = useState("");
//   const [broj, setBroj] = useState("");

  const RegisterHandler= async (event)=>
  {
    event.preventDefault();
    console.log(ime,prezime,email,password,datum);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/register",
        {
          ime:ime,
          prezime:prezime,
          email: email,
          datum_rodjenja:datum,
          sifra: password,
          //datum_rodjenja
        },
        {
          headers: {
            "Content-Type": "application/json",
            // Dodajte dodatne zaglavlja ako su potrebna (npr. autorizacija)
          },
        }
      );

      console.log(response);

      if (response.status === 201) {
        if (response.data.message === "SUCCESS") {
          console.log("Poruka o uspešnoj prijavi:", response.data.message);
          navigate("/");
          return response.data;
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
      // Uhvatite i obradite grešku ako se desi, ovo se odnosi na greške koje nisu vezane za statusni kod odgovora (npr. problem sa mrežom, itd.)
      console.error("Došlo je do greške prilikom prijave:", error);
      window.confirm("Neuspešna prijava!");
    
    }
  }
  const handleEmailChange = (event) => {
   
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };


  const handleImelChange = (event) => {
    setIme(event.target.value);
  };

  const handlePrezimeChange = (event) => {
    setprezime(event.target.value);
  };

  const handleDatumRodjenjaChange = (event) => {
    const selectedDate = event.target.value;
    let datum=selectedDate+"";
    setDatum(datum);
    // Postavite odabrani datum u stanje ili na drugi način rukujte njime
  };
  
//   const handleGradChange = (event) => {
//     setGrad(event.target.value);
//   };

//   const handleUlicaChange = (event) => {
//     setulica(event.target.value);
//   };
//   const handleBrojChange = (event) => {
//     setBroj(event.target.value);
//   };


   const LoginHandler= ()=>
  {
    navigate('/');
  };


    return (
<div id="algn">
        <div id="containerregister">
          <p className="head">Register</p>
          <form action="/" className="input-container">
            <input type="text" placeholder="Ime" className="inpt" onChange={handleImelChange} required />
            <input type="text" placeholder="Prezime" className="inpt" onChange={handlePrezimeChange} required />
            <input type="email" placeholder="Enter email" className="inpt" onChange={handleEmailChange} required />
            <input type="password" placeholder="Enter password" className="inpt" onChange={handlePasswordChange} required />
            <input type="date" className="inpt" onChange={handleDatumRodjenjaChange} required />
            {/* <input type="text" placeholder="Ulica" className="inpt" required  onChange={handleUlicaChange}/>
            <input type="text" placeholder="Grad" className="inpt" required onChange={handleGradChange} />
            <input type="text" placeholder="Broj" className="inpt" onChange={handleBrojChange} required /> */}

            <div className="rem-forgot">
              <div className="rem">
                <input type="checkbox" id="rem-tik" />
                <label htmlFor="rem-tik">Remember me</label>
              </div>
              <span><a href="#">Forgot password</a></span>
            </div>
            <button  className="btn" onClick={RegisterHandler}>Register</button>
          </form>
          <p className="footer" onClick={LoginHandler}>Vec imate akaunt?  <a href="#">Login</a></p>
        </div>
      </div>
    );

}

export default Register;