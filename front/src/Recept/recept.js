// LinkedInStatus.js
import React, { useState } from 'react';
import './recept.css'; // Dodajte stilove
import Link from '@mui/material/Link';
import AccessibilityIcon from '@mui/icons-material/Accessibility';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import CommentIcon from '@mui/icons-material/Comment';
import { IconButton } from '@mui/material';
import StarsIcon from '@mui/icons-material/Stars';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';


const Recept = ({naziv,opis,sastojci, ime,email,prezime}) => {
  const [showAdditionalText, setShowAdditionalText] = useState(false);
  const [nacinPripreme, setnacinPripreme] = useState(false);

  const handleLabelClick = () => {
    setShowAdditionalText(!showAdditionalText);
  };

  const nacinPripremeHandler= ()=>
  {
    setnacinPripreme(!nacinPripreme);
  }


  const LikeHandler= ()=>
  {
    console.log("Lajkovano");// poziva se metoda za lajk 
  }
  return (
    <div className="profile">
         <div className="pocetni">
                <div className="name">{ime} {prezime}  </div>
                <div className="email">{email}</div>
         </div>
      <div className="status">{naziv}</div>
    
      <div className="label dodatni" onClick={handleLabelClick}>
        <Link underline="hover">
          {'Sastojci'}   <KeyboardArrowDownIcon> </KeyboardArrowDownIcon>
        </Link>
          
      </div>
       
      {showAdditionalText && (
        <div className="additional-text dodatni">
         
         
          <ul>
            {sastojci.map((sastojak, index) => (
              <li key={index}>{sastojak}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="label dodatni" onClick={nacinPripremeHandler}>
        <Link underline="hover">
          {'Nacin pripreme'}  <KeyboardArrowDownIcon> </KeyboardArrowDownIcon>
        </Link>
          
      </div>

      {nacinPripreme && (
        <div className="additional-text dodatni">
         {opis}
              
        </div>
      )}




       
      <div className="actions">
       
             
        <IconButton className="like" color="primary" onClick={LikeHandler}>
          <ThumbUpIcon />
        </IconButton>
        
  


    <IconButton>
      <CommentIcon style={{ fontSize: 45 }} />
    </IconButton>

        
      </div>
    </div>
  );
}

export default Recept;
