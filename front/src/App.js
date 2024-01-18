import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login/login';
import Register from './Register/register';
import Recept from './Recept/recept';
import Home from './Home/home';
import PrimarySearchAppBar from './Navbar/navbar';


function App() {
  return (
    <Router>

      <Routes>
        <Route path="/" element={<Login /> } />
        <Route path="/register" element={<Register />} />
        <Route path="/recept" element={<Recept />} />
       <Route path= "/home" element= {<Home></Home>}> </Route>

        //<Route paht="/home1" element={<PrimarySearchAppBar> </PrimarySearchAppBar>}> </Route>
      
      </Routes>
     
      
    </Router>
  );
}

export default App;
