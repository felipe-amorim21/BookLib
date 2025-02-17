// src/context/UserContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';
import axios from 'axios';

const UserContext = createContext();

export const useUser = () => {
    return useContext(UserContext);
};

export const UserProvider = ({ children }) => {
    const [cookies] = useCookies(['access_token']);
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                let token = cookies.access_token;
                if (!token) {
                    setError('Token não encontrado.');
                    return;
                }

                const authHeader = `Bearer ${token}`;
                const response = await axios.get('http://localhost:8000/api/v1/user/me', {
                    headers: {
                        Authorization: authHeader,
                    },
                    withCredentials: true,
                });

                setUserData(response.data);
            } catch (error) {
                setError('Falha ao carregar dados do usuário.');
            }
        };

        if (cookies.access_token) {
            fetchUserData();
        } else {
            setError('Usuário não autenticado.');
        }
    }, [cookies.access_token]);

    return (
        <UserContext.Provider value={{ userData, error, setUserData }}>
            {children}
        </UserContext.Provider>
    );
};
