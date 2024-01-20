import React, { useEffect, useState } from "react";
import "./dodavanjeRecepta.css"; // Uvoz CSS fajla
import axios from "axios";
import { Checkbox, FormControlLabel, Input, TextField } from "@mui/material";
import { CheckBox } from "@mui/icons-material";
import PrimarySearchAppBar from "../Navbar/navbar";

function DodavanjeRecepte() {
  const storedUsername = localStorage.getItem("username");
  const [inputValue, setInputValue] = React.useState("");
  const [opisPripreme, setopisPripreme] = useState("");
  const [kategorija, setKategorija] = useState("");

  const [sastojci, setSastojci] = useState([]);

  const [selektovaniSastojci, setSelektovaniSastojci] = useState([]); // ovo je za checkBox

  useEffect(() => {
    vratiRecepte();
  }, []);

  const nazivRecepta = (event) => {
    setInputValue(event.target.value);
  };

  


  const vratiRecepte = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/vratiSastojke", {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.status === 200) {
        setSastojci(response.data.sastojci);
        console.log(sastojci);
      } else {
        // Ako server nije vratio status 200 OK, obradite to prema potrebi
        console.error("Neuspešan zahtev, statusni kod:", response.status);
      }
    } catch (error) {
      // Uhvatite i obradite grešku ako se desi, ovo se odnosi na greške koje nisu vezane za statusni kod odgovora (npr. problem sa mrežom, itd.)
      console.error("Došlo je do greške prilikom zahteva:", error);
      window.confirm("Došlo je do greške prilikom zahteva!");
    }
  };

  const handleDodajRecept = async () => {
      const formatiraniSastojci = selektovaniSastojci.map(({ naziv, kolicina }) => `${kolicina}gr ${naziv}`);
      console.log(formatiraniSastojci);
    try {
      const obj = {
        naziv: inputValue,
        opis_pripreme: opisPripreme,
        sastojci: formatiraniSastojci,
        kategorija: kategorija,
        email: storedUsername,
      };

      
      console.log(obj);
      const response = await axios.post(
        "http://127.0.0.1:5000/dodajRecept",
        obj,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Odgovor od servera:", response.data);
      // Ovde možete dalje obraditi odgovor sa servera
    } catch (error) {
      console.error("Došlo je do greške prilikom slanja zahteva:", error);
      // Ovde možete obraditi grešku, npr. prikazati korisniku poruku o grešci
    }
  };

  const handleInputChange = (naziv, kolicina) => {
    setSelektovaniSastojci((prevSelektovani) => {
        const updatedSastojci = prevSelektovani.map((prevSastojak) =>
            prevSastojak.naziv === naziv ? { ...prevSastojak, kolicina } : prevSastojak
        );
        return updatedSastojci;
    });
};

  
  const handleCheckboxChange = (naziv, kolicina) => {
    setSelektovaniSastojci((prevSelektovani) => {
      const isChecked = prevSelektovani.some(
        (prevSastojak) => prevSastojak.naziv === naziv
      );
  
      if (isChecked) {
        // Ako je sastojak već selektovan, uklonite ga iz niza
        return prevSelektovani.filter((sastojak) => sastojak.naziv !== naziv);
      } else {
        // Ako sastojak nije selektovan, dodajte ga u niz sa početnom vrednošću količine
        return [...prevSelektovani, { naziv, kolicina }];
      }
    });
  };
  

  const opisHandler = (event) => {
    setopisPripreme(event.target.value);
  };

  const kategorijaHandler = (event) => {
    setKategorija(event.target.value);
  };

  return (

   <div>     <PrimarySearchAppBar> </PrimarySearchAppBar>

    <div className="unos-podataka-forma">
      <Input
        aria-label="Demo input"
        placeholder="Naziv recepta"
        value={inputValue}
        onChange={nazivRecepta}
      />

      <TextField
        id="outlined-multiline-flexible"
        label="Komentar o receptu"
        multiline
        maxRows={4}
        value={opisPripreme}
        onChange={opisHandler}
      />

      <label htmlFor="sastojci">Sastojci:</label>
      {sastojci.map((sastojak, index) => (
  <div key={index} style={{ display: "flex", alignItems: "center" }}>
   <TextField
  id={`outlined-number-${index}`}
  label="Number"
  type="number"
  InputLabelProps={{
    shrink: true,
  }}
  style={{ width: "80px", marginRight: "8px" }}
  value={
    selektovaniSastojci.find(
      (prevSastojak) => prevSastojak.naziv === sastojak.naziv
    )?.kolicina ?? ""
  }
  onChange={(e) =>
    handleInputChange(sastojak.naziv, parseInt(e.target.value, 10) || "")
  }
/>

    <FormControlLabel
      control={
        <Checkbox
          checked={selektovaniSastojci.some(
            (prevSastojak) => prevSastojak.naziv === sastojak.naziv
          )}
          onChange={() => handleCheckboxChange(sastojak.naziv, 0)} // Ovde možete postaviti početnu vrednost količine ako je potrebno
        />
      }
      label={sastojak.naziv}
    />
  </div>
))}






      <Input
        aria-label="Demo input"
        placeholder="Kategorija"
        value={kategorija}
        onChange={kategorijaHandler}
      />

      <button onClick={handleDodajRecept}>Potvrdi</button>
    </div>

    </div>
  );
}

export default DodavanjeRecepte;
