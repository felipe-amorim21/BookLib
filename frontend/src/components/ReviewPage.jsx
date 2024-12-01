import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { saveReview, getBookById } from '../service/apiService';

const ReviewPage = () => {
  const { bookId } = useParams(); // Obtém o id do livro da URL
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [review, setReview] = useState('');

  useEffect(() => {
    const fetchBook = async () => {
      const data = await getBookById(bookId);
      setBook(data);
    };
    fetchBook();
  }, [bookId]);

  const handleSubmit = async () => {
    if (review.trim() === '') {
      alert('Por favor, escreva uma review!');
      return;
    }

    // Salvar a review no banco de dados
    await saveReview(bookId, review);
    // Redirecionar para a página inicial ou a página do livro
    navigate('/');
  };

  return (
    <div className="review-page">
      {book ? (
        <>
          <h2>Escrever Review para: {book.title}</h2>
          <textarea
            value={review}
            onChange={(e) => setReview(e.target.value)}
            placeholder="Escreva sua review aqui"
          />
          <button onClick={handleSubmit}>Salvar Review</button>
        </>
      ) : (
        <p>Carregando livro...</p>
      )}
    </div>
  );
};

export default ReviewPage;
