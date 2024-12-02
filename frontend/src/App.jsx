import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LoginForm } from './components/LoginForm';
import { Home } from './components/Home';
import { RegisterForm } from './components/RegisterForm';
import TestAPI from './components/testBook';
import SearchBooks from './components/searchBooks';
import ReviewPage from './components/ReviewPage';
import BookPage from './components/BookPage';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/home" element={<Home/>} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/test" element={<TestAPI />} />
          <Route path="/books" element={<SearchBooks />} />
          <Route path="/review/:bookId" element={<ReviewPage />} />
          <Route path="/book/:bookId" element={<BookPage />} />

        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
