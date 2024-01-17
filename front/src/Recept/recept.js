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

const Recept = () => {
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
                <div className="name">Ime Prezime   </div>
                <div className="email">email@example.com</div>
         </div>
      <div className="status">Ovo je moj status na LinkedIn-u. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
    
      <div className="label dodatni" onClick={handleLabelClick}>
        <Link underline="hover">
          {'Sastojci'} 
        </Link>
           <KeyboardArrowDownIcon> </KeyboardArrowDownIcon>
      </div>
       
      {showAdditionalText && (
        <div className="additional-text dodatni">
          <AccessibilityIcon />
         Ovde ce da se pobroje svi sastojci i mogu da se koriste <li> </li>
        </div>
      )}

      <div className="label dodatni" onClick={nacinPripremeHandler}>
        <Link underline="hover">
          {'Nacin pripreme'} 
        </Link>
           <KeyboardArrowDownIcon> </KeyboardArrowDownIcon>
      </div>

      {nacinPripreme && (
        <div className="additional-text dodatni">
          <AccessibilityIcon />
            Ovde ce da bude nacin pripreme, kratak opis  
        </div>
      )}




       
      <div className="actions">
       
             
        <IconButton className="like" color="primary" onClick={LikeHandler}>
          <ThumbUpIcon />
        </IconButton>
        
      </div>
    </div>
  );
}

export default Recept;
