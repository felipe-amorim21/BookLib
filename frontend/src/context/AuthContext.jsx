import React, { createContext, useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types'; 
import { jwtDecode } from "jwt-decode";
import Cookies from 'js-cookie';

let jwt_decode = jwtDecode;

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');  
    if (token) {
      fetchUserData(token);
    } else {
        const token = Cookies.get('access_token');
        if (token) {
            fetchUserData(token);
        } else {
            setLoading(false);
        }
    }
  }, []);

  const fetchUserData = async (token) => {
    try {
      const decoded = jwt_decode(token);
      const userId = decoded.sub;

      const response = await fetch(`http://localhost:8000/api/v1/users/${userId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const userData = await response.json();
      console.log("userData: ", userData);
      localStorage.setItem("token", token);
      setUser(userData);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      localStorage.removeItem('token');
      setUser(null);
      setLoading(false);
    }
  };

  const login = async (token) => {
    localStorage.setItem('token', token);
    await fetchUserData(token);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      logout, 
      loading,
      isAuthenticated: !!user 
    }}>
      {children}
    </AuthContext.Provider>
  );
};


AuthProvider.propTypes = {
  children: PropTypes.node.isRequired, 
};

export const useAuth = () => useContext(AuthContext);
