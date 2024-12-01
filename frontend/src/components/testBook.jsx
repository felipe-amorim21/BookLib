import React, { useEffect, useState } from 'react';
import { getBooks, createBook } from '../service/apiService';

const TestAPI = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    // Testar a função de obter todos os livros
    const fetchBooks = async () => {
      try {
        const data = await getBooks();
        setBooks(data);
      } catch (error) {
        console.error('Erro ao buscar livros:', error);
      }
    };

    fetchBooks();
  }, []);

  const handleAddBook = async () => {
    const newBook = {
      title: 'Novo Livro',
      author: 'Autor Exemplo',
      description: 'Descrição do novo livro.',
      genre: 'Ficção',
      published_year: 2024,
    };

    try {
      const createdBook = await createBook(newBook);
      setBooks([...books, createdBook]);
    } catch (error) {
      console.error('Erro ao criar livro:', error);
    }
  };

  return (
    <div>
      <h1>Livros</h1>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            {book.title} - {book.author}
          </li>
        ))}
      </ul>

      <button onClick={handleAddBook}>Adicionar Livro</button>
    </div>
  );
};

export default TestAPI;
