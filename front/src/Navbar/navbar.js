import * as React from "react";
import { styled, alpha } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import InputBase from "@mui/material/InputBase";
import Badge from "@mui/material/Badge";
import MenuItem from "@mui/material/MenuItem";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";
import AccountCircle from "@mui/icons-material/AccountCircle";
import MailIcon from "@mui/icons-material/Mail";
import NotificationsIcon from "@mui/icons-material/Notifications";
import MoreIcon from "@mui/icons-material/MoreVert";
import AddIcon from "@mui/icons-material/Add";
import SendIcon from "@mui/icons-material/Send";
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { InputAdornment, TextField } from "@mui/material";

const Search = styled("div")(({ theme }) => ({
  position: "relative",
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  "&:hover": {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: "100%",
  [theme.breakpoints.up("sm")]: {
    marginLeft: theme.spacing(3),
    width: "auto",
  },
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: "100%",
  position: "absolute",
  pointerEvents: "none",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: "inherit",
  "& .MuiInputBase-input": {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("md")]: {
      width: "20ch",
    },
  },
}));

export default function PrimarySearchAppBar({
  setujFiltriraniRecepti,
  ucitajsveRecepte,
}) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = React.useState(null);
  const [searchValue, setSearchValue] = React.useState("");

  const [donjaGranica, setDonjaGranica] = React.useState('');
  const [gornjaGranica, setGornjaGranica] = React.useState('');

  const storedUsername = localStorage.getItem('username');

  // const [filtriraniRecepte, setfiltriraniRecepte]= React.useState([]);

  const navigate = useNavigate();

  const isMenuOpen = Boolean(anchorEl);
  const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);


  const [showMyRecipes, setShowMyRecipes] = React.useState(false);

  const toggleRecipesHandler = async () => {
    // Ovde možete dodati logiku za dohvatanje i prikazivanje recepata
    setShowMyRecipes((prevValue) => !prevValue);
    console.log(showMyRecipes);

    if(showMyRecipes==true)
    {
      ucitajsveRecepte();
    }
    else
    {
      vratiSamoMojerecepteHandler();
    }
  };


  const PrebaciNaNovuStranicu = () => {
    navigate("/dodavanjeRecepta");
  };
  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const filtriraj = async () => {
    if (searchValue == "") {
      ucitajsveRecepte();
    } else {
      try {
        //  console.log(obj);
        const response = await axios.post(
          "http://127.0.0.1:5000/receptiPoKategoriji",
          {
            kategorija: searchValue,
          }
        );

        console.log("Odgovor od servera:", response.data);
        setujFiltriraniRecepti(response.data.recepti);

        // Ovde možete dalje obraditi odgovor sa servera
      } catch (error) {
        console.error("Došlo je do greške prilikom slanja zahteva:", error);
        // Ovde možete obraditi grešku, npr. prikazati korisniku poruku o grešci
      }
    }
  };

  const handleMobileMenuClose = () => {
    setMobileMoreAnchorEl(null);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    navigate("/home");
    // handleMobileMenuClose();
  };

  const handleMobileMenuOpen = (event) => {
    setMobileMoreAnchorEl(event.currentTarget);
  };

  const handleSearchChange = (event) => {
    setSearchValue(event.target.value);
    console.log(event.target.value);
    if (event.target.value == "") {
      ucitajsveRecepte();
    }
  };

 const receptiPoCeniHandler = async  () => {
   
       try {
          const response = await axios.post('http://127.0.0.1:5000/receptiPoCeni',
         {
           cenaOd:donjaGranica,
           cenaDo:gornjaGranica
          },
          {
            headers:{
                "Content-Type": "application/json",
            }
          }
          );
          console.log(response.data);

          setujFiltriraniRecepti(response.data.recepti);

         //setRecepti(response.data.recepti);
         // Ovdje možete obraditi odgovor od servera
        } catch (error) {
          console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
        }
      };

      const vratiSamoMojerecepteHandler = async  ()=>
      {
       
       
           try {
              const response = await axios.post('http://127.0.0.1:5000/receptiKorisnika',
             {
               email:storedUsername
              },
              {
                headers:{
                    "Content-Type": "application/json",
                }
              }
              );
              console.log(response.data);
    
              setujFiltriraniRecepti(response.data.recepti);
    
             //setRecepti(response.data.recepti);
             // Ovdje možete obraditi odgovor od servera
            } catch (error) {
              console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
            }
      };
  
  

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    console.log("Pretraga:", searchValue);
    // Ovde možete dodati logiku za obradu pretrage ili pozvati funkciju za pretragu
  };

  const receptiPratiocaHandler=  async ()=>
  {
    try {
      const response = await axios.post('http://127.0.0.1:5000/receptiKorisnikaKojePratim',
     {
       korisnik:storedUsername
      },
      {
        headers:{
            "Content-Type": "application/json",
        }
      }
      );
      console.log(response.data);

      setujFiltriraniRecepti(response.data.recepti);

     //setRecepti(response.data.recepti);
     // Ovdje možete obraditi odgovor od servera
    } catch (error) {
      console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
    }
  };

  const menuId = "primary-search-account-menu";
  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
      id={menuId}
      keepMounted
      transformOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
      open={isMenuOpen}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={handleMenuClose}>Home</MenuItem>
    </Menu>
  );

  const mobileMenuId = "primary-search-account-menu-mobile";
  const renderMobileMenu = (
    <Menu
      anchorEl={mobileMoreAnchorEl}
      anchorOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
      id={mobileMenuId}
      keepMounted
      transformOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
      open={isMobileMenuOpen}
      onClose={handleMobileMenuClose}
    >
      <MenuItem>
        <IconButton size="large" aria-label="show 4 new mails" color="inherit">
          <Badge badgeContent={4} color="error">
            <MailIcon />
          </Badge>
        </IconButton>
        <p>Messages</p>
      </MenuItem>
      <MenuItem>
        <IconButton
          size="large"
          aria-label="show 17 new notifications"
          color="inherit"
        >
          <Badge badgeContent={17} color="error">
            <NotificationsIcon />
          </Badge>
        </IconButton>
        <p>Notifications</p>
      </MenuItem>
      <MenuItem onClick={handleProfileMenuOpen}>
        <IconButton
          size="large"
          aria-label="account of current user"
          aria-controls="primary-search-account-menu"
          aria-haspopup="true"
          color="inherit"
        >
          <AccountCircle />
        </IconButton>
        <p>Profile</p>
      </MenuItem>
    </Menu>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ display: { xs: "none", sm: "block" } }}
          >
            MUI
          </Typography>
          <Search>
            <SearchIconWrapper onClick={handleSearchSubmit}>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
            style={{width:'150px'}}
              placeholder="Search…"
              inputProps={{ "aria-label": "search" }}
              onChange={handleSearchChange}
              onClick={handleSearchSubmit}
              value={searchValue}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSearchSubmit(e);
                }
              }}
            />
            <IconButton>
              <SendIcon
                style={{ fontSize: 25, color: "rgb(255, 255, 255)" }}
                onClick={filtriraj}
              >
                {" "}
              </SendIcon>
            </IconButton>
          </Search>

          <div style={{ display: "flex", alignItems: "center" }}>
            <p style={{ margin: 0 }}>Dodaj recept </p>
            <IconButton>
              <AddIcon
                style={{ marginLeft: "2px", color:'white' }}
                size="large"
                onClick={PrebaciNaNovuStranicu}
              />
            </IconButton>
          </div>

          <TextField 
           style={{width:'200px'}}
        label="Donja granica"
        sx={{ m: 1, width: "25ch" }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start" style={{ marginLeft: "2px", color: 'white' }}>rsd</InputAdornment>
          ),
        }}
        value={donjaGranica}
        onChange={(e) => setDonjaGranica(e.target.value)}
      />

      <TextField
       style={{width:'200px'}}
        label="Gornja granica"
        sx={{ m: 1, width: "25ch" }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">rsd</InputAdornment>
          ),
        }}
        value={gornjaGranica}
        onChange={(e) => setGornjaGranica(e.target.value)}
      />

          <IconButton>
            <SendIcon
              style={{ fontSize: 25, color: "rgb(255, 255, 255)" }}
              onClick={receptiPoCeniHandler}
            >
             
            </SendIcon>
          </IconButton>

          <div>
      <div style={{ display: "flex", alignItems: "center" }}>
        <p style={{ margin: 0 }}>
          {showMyRecipes ? "Prikazi sve recepte" : "Prikazi moje recepte"}
        </p>
        <IconButton>
          <AddIcon
            style={{ marginLeft: "2px", color: 'white' }}
            size="large"
            onClick={toggleRecipesHandler}
          />
        </IconButton>
      </div>
      {/* Ostatak vašeg koda */}
    </div>


    <div style={{ display: "flex", alignItems: "center" }}>
            <p style={{ marginLeft: '25px' }}>Recepti pratioca </p>
            <IconButton>
              <VisibilityIcon
                style={{ marginLeft: "2px", color:'white' }}
                size="large"
                onClick={receptiPratiocaHandler}
              />
            </IconButton>
          </div>



    

          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: { xs: "none", md: "flex" } }}>
           
          
            
            <IconButton
              size="large"
              edge="end"
              aria-label="account of current user"
              aria-controls={menuId}
              aria-haspopup="true"
              onClick={handleProfileMenuOpen}
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
          </Box>
          <Box sx={{ display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="show more"
              aria-controls={mobileMenuId}
              aria-haspopup="true"
              onClick={handleMobileMenuOpen}
              color="inherit"
            >
              <MoreIcon />
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>
      {renderMobileMenu}
      {renderMenu}
    </Box>
  );
}
