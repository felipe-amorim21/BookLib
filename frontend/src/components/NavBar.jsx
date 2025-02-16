import React from 'react';
import './css/NavBar.css';
import { useUser } from '../context/userContext';
const NavBar = () => {
const { userData, error } = useUser();


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
            
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default NavBar;
