import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createReview, getBookByGoogleId } from '../service/apiService';
import { useAuth } from '../context/AuthContext'; // Importa o contexto de autenticação

const ReviewPage = () => {
  const { bookId } = useParams(); // Obtém o ID do livro da URL
  const navigate = useNavigate();
  const { user, loading } = useAuth(); // Obtém o usuário autenticado e estado de carregamento
  const [book, setBook] = useState(null);
  const [review, setReview] = useState('');
  const [rating, setRating] = useState(1); // Estado para o rating

  useEffect(() => {
    const fetchBook = async () => {
      const data = await getBookByGoogleId(bookId);
      setBook(data);
    };
    fetchBook();
  }, [bookId]);

  const handleSubmit = async () => {
    if (!user) {
      alert('Você precisa estar logado para criar uma review.');
      return;
    }

    if (review.trim() === '') {
      alert('Por favor, escreva uma review!');
      return;
    }

    const reviewData = {
      book_id: book.id, // ID do livro (assumindo que o retorno do backend tem um ID interno)
      user_id: user.id, // ID do usuário autenticado
      review: review,
      rating: rating,
    };

    try {
      // Salvar a review no banco de dados
      await createReview(reviewData);
      alert('Review salva com sucesso!');
      // Redirecionar para a página do livro
      navigate(`/books`);
    } catch (error) {
      console.error('Erro ao salvar a review:', error);
      alert('Ocorreu um erro ao salvar a review.');
    }
  };

  if (loading) {
    return <p>Carregando...</p>;
  }

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
          <div>
            <label htmlFor="rating">Avaliação: </label>
            <select
              id="rating"
              value={rating}
              onChange={(e) => setRating(Number(e.target.value))}
            >
              {[1, 2, 3, 4, 5].map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>
          <button onClick={handleSubmit}>Salvar Review</button>
        </>
      ) : (
        <p>Carregando livro...</p>
      )}
    </div>
  );
};

export default ReviewPage;
