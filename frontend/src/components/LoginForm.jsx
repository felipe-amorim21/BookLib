import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { useCookies } from "react-cookie";

export const LoginForm = () => {
    const navigate = useNavigate();
    const [, setCookie] = useCookies(["session"]);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSuccess = async (credentialResponse) => {
        try {
            const tokenId = credentialResponse.credential;
            
            // Redireciona o usuário para a rota de login com Google no backend
            window.location.href = `http://localhost:8000/api/v1/auth/google/login?credential=${tokenId}`;
            document.cookie = `access_token=${tokenId}; path=/; secure=true; SameSite=Strict`;

        } catch (error) {
            console.error("Erro ao autenticar:", error);
            alert("Falha no login. Tente novamente.");
        }
    };

    const handleFailure = (error) => {
        console.error("Erro no login do Google:", error);
        alert("Erro no login com Google. Tente novamente.");
    };

    const handleLogin = async (event) => {
        event.preventDefault();
        setError("");

        try {
            const response = await fetch("http://localhost:8000/api/v1/login", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/x-www-form-urlencoded" 
                },
                body: new URLSearchParams({
                    username: email,   
                    password: password 
                }),
            });

            if (!response.ok) {
                throw new Error("Credenciais inválidas");
            }

            const data = await response.json();
            setCookie("access_token", data.access_token, { path: "/", secure: true, sameSite: "Strict" });
            //alert("Login realizado com sucesso!");
            //navigate("/books");
            navigate("/home");
            window.location.reload();

        } catch (err) {
            console.error("Erro no login:", err);
            setError("Erro ao fazer login. Verifique suas credenciais.");
        }
    };

    const handleRegisterRedirect = () => {
        navigate("/register");
    };

    return (
        <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "100px" }}>
                <h1>Login</h1>

                <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ marginBottom: "10px", padding: "8px", width: "300px" }}
                    />
                    <input
                        type="password"
                        placeholder="Senha"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ marginBottom: "10px", padding: "8px", width: "300px" }}
                    />
                    {error && <p style={{ color: "red" }}>{error}</p>}
                    <button type="submit" style={{ padding: "10px 20px", cursor: "pointer" }}>
                        Login
                    </button>
                </form>

                <hr style={{ width: "100%", margin: "20px 0" }} />

                <GoogleLogin onSuccess={handleSuccess} onError={handleFailure} />

            
                <div style={{ marginTop: "20px", textAlign: "center" }}>
                    <p>Não tem uma conta? <button className="text-blue-600 hover:text-blue-800 cursor-pointer" onClick={handleRegisterRedirect} >Cadastre-se</button></p>
                </div>
            </div>
        </GoogleOAuthProvider>
    );
};
