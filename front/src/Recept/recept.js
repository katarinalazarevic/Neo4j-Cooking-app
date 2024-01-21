// LinkedInStatus.js
import React, { useEffect, useState } from "react";
import "./recept.css"; // Dodajte stilove
import Link from "@mui/material/Link";
import AccessibilityIcon from "@mui/icons-material/Accessibility";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import CommentIcon from "@mui/icons-material/Comment";
import { Button, IconButton, TextField } from "@mui/material";
import StarsIcon from "@mui/icons-material/Stars";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import Box from "@mui/material/Box";
import Rating from "@mui/material/Rating";
import Typography from "@mui/material/Typography";
import SendIcon from '@mui/icons-material/Send';
import axios from "axios";


const Recept = ({ naziv, opis, sastojci, ime, email, prezime ,ocena, recept}) => {
  const [showAdditionalText, setShowAdditionalText] = useState(false);
  const [showComment, setshowComment] = useState(false);
  const [nacinPripreme, setnacinPripreme] = useState(false);
  const [value, setValue] = React.useState(2);
  const [commentText, setCommentText] = useState('');
  const [komentari, setKomentari] = useState([]);
  const [showALLComments, setshowALLComments]= useState(false);

  //console.log(recept.recept.sastojci);

  useEffect(()=>
  {
      ucitajKomentareRecepta();
     // console.log("email je", email );
  },[])


  const ucitajKomentareRecepta = async ()=>
  {
      try{
          const response= await axios.post(
            "http://127.0.0.1:5000/komentariZaRecept",
            {
              naziv_recepta: naziv
            },
            {
              headers: {
                "Content-Type": "application/json",
              }
            }
          );
          console.log(response.data);
          setKomentari(response.data.komentari)
      }
      catch(error)
      {
        console.error(error);
      }
  };

  const handleSendClick =  async ()  => {
    // Ovde možeš ispisati vrednost unetu u TextField u konzoli
    console.log(commentText);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/dodajKomentar",
        {
          korisnik_email: email,
          sadrzaj: commentText,
          naziv_recepta: naziv
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
  
      console.log(response.data); // Ovde možeš raditi nešto sa odgovorom iz servera
      window.confirm("Komentar uspesno dodat!");
    } catch (error) {
      console.error("Greška prilikom slanja zahteva:", error);
    }

    
  };

  const AllComentsHandler= ()=>
  {
    setshowALLComments(!showALLComments);
  }

  const handleLabelClick = () => {
    setShowAdditionalText(!showAdditionalText);
  };

  const nacinPripremeHandler = () => {
    setnacinPripreme(!nacinPripreme);
  };

  const handleRatingChange = (event, newValue) => {
    setValue(newValue);
    // Ovde možeš odštampati vrednost ocene na konzoli
    console.log('Nova vrednost ocene:', newValue);
  };

  const commentHandler= ()=>
  {
    setshowComment(!showComment);
  };

  const postaviOcenu=  async ()=>
  {
    try {
      const obj = {
        ocena: value,
        naziv_recepta: naziv,
        
        
      };

      
      console.log(obj);
      const response = await axios.post(
        "http://127.0.0.1:5000/dodajOcenuReceptu",
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

  }



  return (
    <div className="profile">
      <div className="pocetni">
        <div className="name">
          {ime} {prezime}{" "}
        </div>
        <div className="email">{email}</div>
      </div>
      <div className="status">
  <h2 style={{ display: 'inline-block', marginRight: '10px' }}>{naziv}</h2>
  <h5 style={{ display: 'inline-block' }}>Trenutna ocena: <span style={{ color: 'red' }}>{ocena}</span>/{5}</h5>
  <p syle={{margin:'0px', padding:'0px'}}> Kategorija recepta:  <span style={{ color: 'red' }}>{recept.kategorija}</span></p>

</div>




      <div
 className="custom-link"
  onClick={handleLabelClick}
    /* Dodaj funkcionalnost koja treba da se izvrši kada se klikne na "Sastojci" */
  
  style={{ cursor: 'pointer', color: 'black' }}
>
  {"Sastojci"} <KeyboardArrowDownIcon />
</div>


      {showAdditionalText && (
        <div className="additional-text dodatni" >
          <ul>
            {sastojci.map((sastojak, index) => (
              <li key={index}>{sastojak}</li>
            ))}
          </ul>
        </div>
      )}

<div
 className="custom-link"
  onClick={nacinPripremeHandler}
    /* Dodaj funkcionalnost koja treba da se izvrši kada se klikne na "Sastojci" */
  
  style={{ cursor: 'pointer', color: 'black' }}
>
  {"Nacin pripreme"} <KeyboardArrowDownIcon />
</div>

      {nacinPripreme && <div className="additional-text dodatni">{opis}</div>}

        <h7 style={{color:'red', marginTop:'20px'}}>Ocenjivanje i komentarisanje</h7>
      <div className="actions" style={{ display: 'flex', alignItems: 'center', marginTop:'0px'}}>
        <Box
          sx={{
            "& > legend": { mt: 2 },
          }}
        >

            <Rating
          name="simple-controlled"
          value={value}
          onChange={handleRatingChange}
        />
        </Box>
        <IconButton>
      <SendIcon style={{fontSize: 25, color: 'rgb(25, 118, 210)' }} onClick={postaviOcenu}> </SendIcon>
      </IconButton>
        <IconButton>
        <CommentIcon  onClick={commentHandler}style={{ fontSize: 45, color: 'rgb(25, 118, 210)' }} />
        </IconButton>


      </div>


     {showComment && (
        <div style={{  border : '1px solid black ', padding:'10px',marginBottom:'5px', width:'200px', borderRadius:'10px'}}>
          <TextField
            id="outlined-multiline-flexible"
            label="Komentar o receptu"
            multiline
            maxRows={4}
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
          />
          <div style={{ marginTop: '10px' }}>
            <Button variant="contained" endIcon={<SendIcon />} onClick={handleSendClick}>
              Send
            </Button>
          </div>
        </div>
      )}

<div
 className="custom-link"
  onClick={AllComentsHandler}
    /* Dodaj funkcionalnost koja treba da se izvrši kada se klikne na "Sastojci" */
  
  style={{ cursor: 'pointer', color: 'black', marginBottom:'10px' }}
>
  {"Komentari "} <KeyboardArrowDownIcon />
</div>
       
<div className="commentsWrapper">
  {showALLComments && (
    <div className="commentsContainer1">
      {komentari.map((komentar, index) => (
        <div key={index} className="commentContainer">
          <h6 style={{ color: 'black', margin: '0' }}>{komentar.korisnik_email}</h6>
          <h3 style={{ color: 'black', margin: '0' }}>{komentar.sadrzaj}</h3>
        </div>
      ))}
    </div>
  )}
</div>




    </div>
  );
};

export default Recept;
