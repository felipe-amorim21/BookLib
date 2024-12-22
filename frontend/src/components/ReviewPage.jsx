import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createReview, getBookByGoogleId } from '../service/apiService';
import { useAuth } from '../context/AuthContext';
import './css/ReviewPage.css';

const ReviewPage = () => {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const { user, loading } = useAuth();
  const [book, setBook] = useState(null);
  const [reviewTitle, setReviewTitle] = useState('');
  const [review, setReview] = useState('');
  const [storyRating, setStoryRating] = useState(3);
  const [styleRating, setStyleRating] = useState(3);
  const [characterRating, setCharacterRating] = useState(3);
  const [recommendation, setRecommendation] = useState(false);

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

    if (review.trim() === '' || reviewTitle.trim() === '') {
      alert('Por favor, preencha o título e a review!');
      return;
    }

    const overallRating = (storyRating + styleRating + characterRating) / 3;

    const reviewData = {
      book_id: book.id,
      user_id: user.id,
      review_title: reviewTitle,
      review,
      story_rating: storyRating,
      style_rating: styleRating,
      character_rating: characterRating,
      overall_rating: overallRating,
      recommendation,
    };

    try {
      await createReview(reviewData);
      alert('Review salva com sucesso!');
      navigate(`/book/${bookId}`);
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
          <input
            type="text"
            value={reviewTitle}
            onChange={(e) => setReviewTitle(e.target.value)}
            placeholder="Título da Review"
          />
          <textarea
            value={review}
            onChange={(e) => setReview(e.target.value)}
            placeholder="Escreva sua review aqui"
          />
          <div>
            <label>História: </label>
            <select
              value={storyRating}
              onChange={(e) => setStoryRating(Number(e.target.value))}
            >
              {[1, 2, 3, 4, 5].map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Estilo de Escrita: </label>
            <select
              value={styleRating}
              onChange={(e) => setStyleRating(Number(e.target.value))}
            >
              {[1, 2, 3, 4, 5].map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Personagens: </label>
            <select
              value={characterRating}
              onChange={(e) => setCharacterRating(Number(e.target.value))}
            >
              {[1, 2, 3, 4, 5].map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>
              <input
                type="checkbox"
                checked={recommendation}
                onChange={(e) => setRecommendation(e.target.checked)}
              />
              Recomenda este livro?
            </label>
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
