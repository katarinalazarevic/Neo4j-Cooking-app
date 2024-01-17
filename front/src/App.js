import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './Login/login';
import Register from './Register/register';

function App() {
  return (
    <Router>
     
      

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
       
      </Routes>
    </Router>
  );
}

export default App;
