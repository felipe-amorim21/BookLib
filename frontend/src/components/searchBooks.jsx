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
  const [noResultsMessage, setNoResultsMessage] = useState('');
  const booksPerPage = 8;
  const navigate = useNavigate();

  const handleSearch = async () => {
    if (!query.trim()) return;
    const results = await searchBooks(query);
    if (results.length === 0) {
      setNoResultsMessage('Nenhum livro encontrado para essa busca.');
    } else {
      setNoResultsMessage('');
    }
    setBooks(results);
    setTotalPages(Math.ceil(results.length / booksPerPage));
    setCurrentPage(1);
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handleScroll = () => {
    setIsSticky(window.scrollY > 100);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const currentBooks = books.slice(
    (currentPage - 1) * booksPerPage,
    currentPage * booksPerPage
  );

  const handleReviewClick = async (e, book ) => {
    e.stopPropagation();
    await saveBookIfNotExist(book);
    navigate(`/review/${book.id}`);
  };

  const handleBookClick = async (book) => {
    await saveBookIfNotExist(book);
    navigate(`/book/${book.id}`);
  };

  return (
    <div className="search-books-container">
      <h1 className="search-title">Buscar Livros</h1>

      <div className={`search-input-container ${isSticky ? 'sticky' : ''}`}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Digite o título ou autor do livro"
          className="search-input"
        />
        <button onClick={handleSearch} className="search-btn">
          Buscar
        </button>
      </div>

      {noResultsMessage && <p className="no-results-message">{noResultsMessage}</p>}

      {books.length > 0 && (
        <div className="books-list">
          <div className="books-grid">
            {currentBooks.map((book) => (
              <div
                key={book.id}
                className="book-item"
                onClick={() => handleBookClick(book)}
              >
                <h3 className="book-title">{book.title}</h3>
                <p className="book-author">
                  <strong>Autor:</strong> {book.author}
                </p>
                {book.thumbnail && (
                  <img
                    src={book.thumbnail}
                    alt={book.title}
                    className="book-thumbnail"
                  />
                )}
                <button className="review-btn" onClick={(e) => handleReviewClick(e, book)}>Escrever Review</button>
              </div>
            ))}
          </div>

          <div className="pagination">
            {[...Array(totalPages).keys()].map((number) => (
              <button
                key={number + 1}
                onClick={() => paginate(number + 1)}
                className={`pagination-btn ${currentPage === number + 1 ? 'active' : ''}`}
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
