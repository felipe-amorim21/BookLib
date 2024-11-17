import React, { useEffect, useState } from "react";
import { useCookies } from "react-cookie";
import axios from "axios";
import { useAuth } from '../context/AuthContext';

export const Home = () => {
    const [cookies] = useCookies(["acess_token"]);
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState("");

    const { user } = useAuth();

    useEffect(() => {
        console.log("cookies: ", cookies.access_token)
        console.log("user: ", user)
        const fetchUserData = async () => {
            try {
                let token = cookies.access_token;
                console.log("token: ", token)
                if (!token) {
                    setError("Token não encontrado.");
                    return;
                }

                
                const authHeader = `Bearer ${token}`;
                const response = await axios.get("http://localhost:8000/api/v1/user/me", {
                    headers: {
                        Authorization: authHeader, 
                    },
                    withCredentials: true,
                });

                setUserData(response.data); 
            } catch (error) {
                console.error("Erro ao obter dados do usuário:", error);
                setError("Falha ao carregar dados do usuário.");
            }
        };

        if (cookies.access_token) {
            fetchUserData(); 
        } else {
            setError("Usuário não autenticado.");
        }
    }, [cookies.access_token]); 

    return (
        <div>
            <h1>Bem-vindo à página inicial</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {userData ? (
                <div>
                    <h2>Informações do Usuário</h2>
                    <p>Nome: {userData.name}</p>
                    <p>Email: {userData.email}</p>
                    
                    {}
                </div>
            ) : (
                <p>Carregando dados do usuário...</p>
            )}
        </div>
    );
};