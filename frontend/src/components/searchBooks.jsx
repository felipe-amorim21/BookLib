import React, { useState, useEffect } from 'react';
import { searchBooks, saveBookIfNotExist } from '../service/apiService';
import { useNavigate } from 'react-router-dom';
import './css/searchBooks.css';

const SearchBooks = () => {
  const [query, setQuery] = useState('');
  const [books, setBooks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isSticky, setIsSticky] = useState(false); 
  const booksPerPage = 8;
  const navigate = useNavigate();

  const handleSearch = async () => {
    if (!query.trim()) return;
    const results = await searchBooks(query);
    setBooks(results);
    setTotalPages(Math.ceil(results.length / booksPerPage)); 
    setCurrentPage(1);
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  // Detectar rolagem
  const handleScroll = () => {
    if (window.scrollY > 100) {
      setIsSticky(true);
    } else {
      setIsSticky(false);
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const currentBooks = books.slice((currentPage - 1) * booksPerPage, currentPage * booksPerPage);

  // Função para abrir a página de review e salvar o livro, se necessário
  const handleReviewClick = async (book) => {
    await saveBookIfNotExist(book);
    navigate(`/review/${book.id}`); // Redireciona para a página de review
  };

  return (
    <div className="search-books-container">
      <h1>Buscar Livros</h1>
      <div className={`search-input-container ${isSticky ? 'sticky' : ''}`}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Digite o título ou autor do livro"
        />
        <button onClick={handleSearch}>Buscar</button>
      </div>

      {books.length > 0 && (
        <div className="books-list">
          <div className="books-grid">
            {currentBooks.map((book) => (
              <div key={book.id} className="book-item" onClick={() => handleReviewClick(book)}>
                <h3>{book.title}</h3>
                <p><strong>Autor:</strong> {book.author}</p>
                {book.thumbnail && <img src={book.thumbnail} alt={book.title} />}
                <button className="review-btn">Escrever Review</button>
              </div>
            ))}
          </div>

          <div className="pagination">
            {[...Array(totalPages).keys()].map((number) => (
              <button
                key={number + 1}
                onClick={() => paginate(number + 1)}
                className={currentPage === number + 1 ? 'active' : ''}
              >
                {number + 1}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBooks;
