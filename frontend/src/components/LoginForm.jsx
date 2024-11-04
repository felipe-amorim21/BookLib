import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AlertCircle, Mail, Lock, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Handle OAuth callback
  useEffect(() => {
    // Check if this is a callback from OAuth
    const error = searchParams.get('error');
    if (error) {
      setError('Login with Google failed. Please try again.');
    }
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await fetch('http://localhost:8000/api/v1/login', {
        method: 'POST',
        body: formData,
        credentials: 'include', // Important for cookies
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      await login(data.access_token);
      navigate('/home');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      
      const response = await fetch('http://localhost:8000/api/v1/auth/google/init', {
        method: 'GET',
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error('Failed to initialize Google login');
      }
      window.location.href = 'http://localhost:8000/api/v1/auth/google/login';
    } catch (err) {
      setError('Failed to start Google login. Please try again.');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md bg-white p-8 rounded shadow-md">
        <h2 className="text-2xl font-bold text-center">Bem-vindo</h2>
        <p className="text-center">Faça login</p>
        
        <form onSubmit={handleSubmit} className="space-y-4 mt-6">
          {error && (
            <div className="alert alert-danger flex items-center mb-4">
              <AlertCircle className="h-4 w-4" />
              <span className="ml-2">{error}</span>
            </div>
          )}
          
          <div className="space-y-1">
            <label htmlFor="email">Email</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                id="email"
                type="email"
                placeholder="joao@exemplo.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="border border-gray-300 rounded py-2 px-10 w-full"
                required
              />
            </div>
          </div>

          <div className="space-y-1">
            <label htmlFor="password">Senha</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="border border-gray-300 rounded py-2 px-10 w-full"
                required
              />
            </div>
          </div>

          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded" disabled={isLoading}>
            {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : 'Logar'}
          </button>
        </form>

        <div className="mt-4">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="bg-white px-2 text-gray-500">Ou entre com</span>
            </div>
          </div>

          <button
            type="button"
            className="mt-4 w-full border border-gray-300 py-2 rounded flex items-center justify-center"
            onClick={handleGoogleLogin}
          >
            <img
              src="/api/placeholder/20/20"
              alt="Google"
              className="mr-2 h-5 w-5"
            />
            Logar com o google
          </button>
        </div>

        <div className="flex justify-center mt-4">
          <p className="text-sm text-gray-600">
            Não tem uma conta?{' '}
            <button
              className="text-blue-600 hover:text-blue-800"
              onClick={() => navigate('/register')}
            >
              Registrar
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};
