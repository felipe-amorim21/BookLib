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

                // Configurar o cabeçalho Authorization dependendo do tipo de token
                const authHeader = `Bearer ${token}`;
                const response = await axios.get("http://localhost:8000/api/v1/user/me", {
                    headers: {
                        Authorization: authHeader, // Usa o token de autenticação
                    },
                    withCredentials: true, // Envia os cookies com a requisição
                });

                setUserData(response.data); // Armazena os dados do usuário na state
            } catch (error) {
                console.error("Erro ao obter dados do usuário:", error);
                setError("Falha ao carregar dados do usuário.");
            }
        };

        if (cookies.access_token) {
            fetchUserData(); // Tenta obter dados do usuário se o token estiver presente
        } else {
            setError("Usuário não autenticado.");
        }
    }, [cookies.access_token]); // Reexecuta quando o cookie mudar

    return (
        <div>
            <h1>Bem-vindo à página inicial</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {userData ? (
                <div>
                    <h2>Informações do Usuário</h2>
                    <p>Nome: {userData.name}</p>
                    <p>Email: {userData.email}</p>
                    
                    {/* Exiba outras informações do usuário conforme necessário */}
                </div>
            ) : (
                <p>Carregando dados do usuário...</p>
            )}
        </div>
    );
};