import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getBookByGoogleId, getReviewsByBookId } from '../service/apiService';

const BookPage = () => {
  const { bookId } = useParams(); // Obtém o ID do livro da URL
  const [book, setBook] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBookAndReviews = async () => {
      try {
        // Obtém os detalhes do livro
        const bookData = await getBookByGoogleId(bookId);
        setBook(bookData);

        // Obtém as reviews do livro
        const reviewsData = await getReviewsByBookId(bookData.id);
        setReviews(reviewsData);
      } catch (error) {
        console.error('Erro ao buscar detalhes do livro e reviews:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBookAndReviews();
  }, [bookId]);

  if (loading) {
    return <p>Carregando...</p>;
  }

  return (
    <div className="book-page">
      {book ? (
        <>
          <h1>{book.title}</h1>
          <img src={book.coverUrl} alt={book.title} style={{ width: '200px', height: 'auto' }} />
          <h2>Reviews</h2>
          {reviews.length > 0 ? (
            <ul>
              {reviews.map((review) => (
                <li key={review.id}>
                  
                  <p><strong>Avaliação:</strong> {review.rating}/5</p>
                  <p>{review.review}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p>Este livro ainda não possui reviews.</p>
          )}
        </>
      ) : (
        <p>Livro não encontrado.</p>
      )}
    </div>
  );
};

export default BookPage;
