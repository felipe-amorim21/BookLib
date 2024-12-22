import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, Mail, User, Lock, Loader2 } from 'lucide-react';
import { Button, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Label, Input, Alert, AlertDescription } from './UIComponents'; // Assume these are your custom UI components

export const RegisterForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords don't match");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      navigate('/login');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md bg-white shadow-md rounded-lg p-8">
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "100px" }}>
      <h1>Cadastro</h1>

        {/* Error Message */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div className="space-y-1">
            <Label htmlFor="email">Email</Label>
            <div className="relative">
              <Input
                id="email"
                type="email"
                placeholder="joao@exemplo.com"
                value={formData.email}
                onChange={handleChange}
                style={{ marginBottom: "10px", padding: "8px", width: "300px" }}
                required
              />
            </div>
          </div>

          <div className="space-y-1">
            <Label htmlFor="username">Usuario</Label>
            <div className="relative">
              <Input
                id="username"
                type="text"
                placeholder="exemplo"
                value={formData.username}
                onChange={handleChange}
                style={{ marginBottom: "10px", padding: "8px", width: "300px" }}
                required
              />
            </div>
          </div>

          <div className="space-y-1">
            <Label htmlFor="password">Senha</Label>
            <div className="relative">
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                style={{ marginBottom: "10px", padding: "8px", width: "300px" }}
                required
              />
            </div>
          </div>

          <div className="space-y-1">
            <Label htmlFor="confirmPassword">Confirmar senha</Label>
            <div className="relative">
              <Input
                id="confirmPassword"
                type="password"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                style={{ marginBottom: "10px", padding: "8px", width: "300px" }}
                required
              />
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              'Cadastrar'
            )}
          </Button>
        </form>
        <hr style={{ width: "100%", margin: "20px 0" }} />
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Já tem uma conta?{' '}
            <button
              className="text-blue-600 hover:text-blue-800 cursor-pointer"
              onClick={() => navigate('/login')}
            >
              Fazer Login
            </button>
          </p>
        </div>
      </div>
    </div>
    </div>
  );
};
