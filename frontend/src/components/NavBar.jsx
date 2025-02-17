import React from 'react';
import './css/NavBar.css';
import { useUser } from '../context/userContext';

const NavBar = () => {
const { userData, setUserData } = useUser();


const clearCookies = () => {
  document.cookie = 'access_token=; Max-Age=0';
};

const handleLogout = (e) => {
  e.preventDefault();
  clearCookies();
  localStorage.removeItem('token');
  setUserData(null);
  window.location.href = '/login'; // Redireciona para a página de login após o logout
};


  return (
    <div className="top-bar">
      <div className="top-bar-content">
        <h1 className="site-title"><a href="/">BookLib</a></h1>
        <nav className="top-nav">
          <ul>
            <li><a href="/books">Livros</a></li>
            {userData ? <li><a href="/favoritos">Favoritos</a></li> : <li><a href="/login">Login</a></li>}
            <li><a href="/about">Sobre</a></li>
            <li><a href="/contact">Contato</a></li>
            {userData && <li><button onClick={handleLogout}>Logout</button></li>}
            
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default NavBar;
