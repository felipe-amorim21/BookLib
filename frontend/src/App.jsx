import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LoginForm } from './components/LoginForm';
import { Home } from './components/Home';
import { RegisterForm } from './components/RegisterForm';
import  About  from './components/About';
import  Contact  from './components/Contact';
import TestAPI from './components/testBook';
import SearchBooks from './components/searchBooks';
import ReviewPage from './components/ReviewPage';
import BookPage from './components/BookPage';
import { UserProvider } from './context/userContext';
import FavoritosPage from './components/FavoritosPage';

const App = () => { 
  return (
    <UserProvider>
      <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home/>} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/test" element={<TestAPI />} />
          <Route path="/books" element={<SearchBooks />} />
          <Route path="/favoritos" element={<FavoritosPage />} />
          <Route path="/review/:bookId" element={<ReviewPage />} />
          <Route path="/book/:bookId" element={<BookPage />} />

        </Routes>
      </Router>
    </AuthProvider>

    </UserProvider>
    
  );
};

export default App;
