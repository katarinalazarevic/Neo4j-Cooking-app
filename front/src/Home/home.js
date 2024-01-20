import React, { useEffect, useState, useContext, useReducer } from "react";
import Recept from "../Recept/recept";
import axios from "axios";
import PrimarySearchAppBar from "../Navbar/navbar";




const Home= ()=>
{
    const [recepti, setRecepti] = useState([]);
    const [novih10, setNovih10]= useState([]);
    const storedUsername = localStorage.getItem('username');
    const storedName = localStorage.getItem('ime');
    const storedPrezime= localStorage.getItem('prezime');

   // const [filtriraniRecepti,setfiltriraniRecepti]= useState([]);
    
    useEffect(()=>
    {
        console.log(storedUsername);
         ucitajRecepte();
         console.log(recepti);
      //console.log(filtriraniRecepti);

    },[])

    
    const ucitajRecepte = async () => {
        try {
          const response = await axios.post('http://127.0.0.1:5000/receptiKorisnika',
         {
            email: storedUsername
          },
          {
            headers:{
                "Content-Type": "application/json",
            }
          }
          );
          console.log(response.data);
          setRecepti(response.data.recepti);
          // Ovdje možete obraditi odgovor od servera
        } catch (error) {
          console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
        }
      };
    
    
    return (
        <div>
            <PrimarySearchAppBar
              //setujFiltriraniRecepti={setfiltriraniRecepti} 
              setujFiltriraniRecepti ={setRecepti}
              ucitajsveRecepte= {ucitajRecepte}
              >
              </PrimarySearchAppBar>
            <div style={{ overflowY: 'scroll', maxHeight: '550px' }}>
        {recepti.map((recept, index) => (
          <Recept
            key={index} // Preporučljivo je koristiti jedinstveni ključ za svaki element u iteraciji
            naziv={recept.naziv}
            opis={recept.opis_pripreme}
            sastojci={recept.sastojci}
            ime={storedName}
            email={storedUsername}
            prezime={storedPrezime}
            ocena={recept.ocena}
          />
        ))}
      </div>






     
       </div>
        

    );

}

export default Home;