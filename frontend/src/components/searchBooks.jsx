import React, { useState } from 'react';
import { searchBooks } from '../service/apiService';

const SearchBooks = () => {
  const [query, setQuery] = useState('');
  const [books, setBooks] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;
    const results = await searchBooks(query);
    setBooks(results);
  };

  return (
    <div>
      <h1>Buscar Livros</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Digite o título ou autor do livro"
      />
      <button onClick={handleSearch}>Buscar</button>

      {books.length > 0 && (
        <ul>
          {books.map((book) => (
            <li key={book.id}>
              <h3>{book.title}</h3>
              <p><strong>Autor:</strong> {book.author}</p>
              {book.thumbnail && <img src={book.thumbnail} alt={book.title} />}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBooks;
