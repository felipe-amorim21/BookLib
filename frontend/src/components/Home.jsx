// src/Home.jsx

import React from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Home = () => {
  const { user } = useAuth();

  console.log("User: ", user)


  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh', // Use full viewport height
      textAlign: 'center',
      padding: '20px',
    }}>
      <h1>Bem-vindo, {user.username}!</h1>
    </div>
  );
};

