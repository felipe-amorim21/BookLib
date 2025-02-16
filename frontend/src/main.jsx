// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import NavBar from './components/NavBar';
import { UserProvider } from './context/userContext';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <UserProvider >
            <NavBar />
            <App />
        </UserProvider>
    </React.StrictMode>
);
