import React, { useEffect, useState } from "react";
import { useCookies } from "react-cookie";
import axios from "axios";
import { useAuth } from '../context/AuthContext';
import './css/Home.css';

export const Home = () => {
    const [cookies] = useCookies(["acess_token"]);
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState("");

    const { user } = useAuth();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                let token = cookies.access_token;
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
            
        }
    }, [cookies.access_token]);

    return (
        <div className="home-container">
            <header className="header">
                <h1 className="app-name">BookLib</h1>
                {user && <p className="welcome-message">Bem-vindo, {user.username}!</p>}
            </header>

            <section className="intro-section">
                <p className="intro-text">
                    O <strong>BookLib</strong> é o sistema ideal para amantes de livros que querem compartilhar suas
                    experiências e opiniões. Faça login para adicionar reviews sobre seus livros favoritos, além de 
                    poder salvar os livros que mais gosta em sua lista de favoritos. 
                    <br />
                    
                </p>
            </section>

            
        </div>
    );
};
