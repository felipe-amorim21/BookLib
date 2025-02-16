import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  getBookByGoogleId,
  getReviewsByBookId,
  getAiReviewByBookId,
  checkIfBookIsFavorited,
  favoriteBook,
  unfavoriteBook,
} from "../service/apiService";
import { useAuth } from '../context/AuthContext'; 
import "./css/BookPage.css";
import { useUser } from '../context/userContext';


const BookDetails = ({ book, isFavorited, handleFavoriteToggle }) => (
  <div className="book-details">
    <h1>{book.title}</h1>
    <img
      src={book.thumbnail}
      alt={`Capa do livro: ${book.title}`}
      className="book-cover"
    />
    <p>
      <strong>Autor:</strong> {book.author}
    </p>
    <p>
      <strong>Publicado em:</strong> {book.publishedDate}
    </p>
    <p>
      <strong>Descrição:</strong> {book.description || "Descrição indisponível."}
    </p>

    {/* Botão de Favoritar/Desfavoritar */}
    <button className="favorite-button" onClick={handleFavoriteToggle}>
      {isFavorited ? "Desfavoritar" : "Favoritar"}
    </button>
  </div>
);

const AiReviewCard = ({ aiReview }) => (
  <div className="review-card ai-review">
    <h3>Resumo geral por IA</h3>
    <p>{aiReview}</p>
  </div>
);

const ReviewList = ({ reviews }) => (
  <div className="review-list">
    <h2>Reviews dos usuários</h2>
    {reviews.length > 0 ? (
      <ul>
        {reviews.map((review) => (
          <li key={review.id} className="review-item">
            <h3>{review.review_title}</h3>
            <p>
              <strong>Avaliação Geral:</strong> {review.overall_rating.toFixed(2)}
            </p>
            <p>
              <strong>História:</strong> {review.story_rating}
            </p>
            <p>
              <strong>Escrita:</strong> {review.style_rating}
            </p>
            <p>
              <strong>Personagens:</strong> {review.character_rating}
            </p>
            <p>
              <strong>Recomenda?</strong> {review.recommendation ? "Sim" : "Não"}
            </p>
            <p>{review.review}</p>
          </li>
        ))}
      </ul>
    ) : (
      <p>Este livro ainda não possui reviews.</p>
    )}
  </div>
);

const BookPage = () => {
  const { bookId } = useParams();
  const [book, setBook] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [aiReview, setAiReview] = useState(null);
  const [isFavorited, setIsFavorited] = useState(false);
  const [loading, setLoading] = useState(true);
  const { userData, error } = useUser();
  console.log("userauth: ", userData);

  useEffect(() => {

    if(!userData){
      return;
    }
    const fetchBookAndReviews = async () => {
      try {
        const bookData = await getBookByGoogleId(bookId);
        setBook(bookData);

        const reviewsData = await getReviewsByBookId(bookData.id);
        setReviews(reviewsData);

        const aiReviewData = await getAiReviewByBookId(bookData.id);
        setAiReview(aiReviewData.ai_review || null);

        // Verifica se o livro já está favoritado
        const favoriteStatus = await checkIfBookIsFavorited(bookData.id, userData);
        setIsFavorited(favoriteStatus.isFavorito);
      } catch (error) {
        console.error("Erro ao buscar detalhes do livro e reviews:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBookAndReviews();
  }, [bookId,userData]);

  const handleFavoriteToggle = async () => {
    if (isFavorited) {
      await unfavoriteBook(book.id, userData);
    } else {
      await favoriteBook(book.id, userData);
    }

    // Atualiza o estado após a ação
    setIsFavorited(!isFavorited);
  };

  if (loading) {
    return <p>Carregando...</p>;
  }

  return (
    <div className="book-page">
      {book ? (
        <>
          <BookDetails
            book={book}
            isFavorited={isFavorited}
            handleFavoriteToggle={handleFavoriteToggle}
          />

          {/* Exibe o resumo da IA se existir */}
          {aiReview && <AiReviewCard aiReview={aiReview} />}

          <ReviewList reviews={reviews} />
        </>
      ) : (
        <p>Livro não encontrado.</p>
      )}
    </div>
  );
};

export default BookPage;
