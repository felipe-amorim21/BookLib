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
import { useNavigate } from 'react-router-dom';
import { FaRegHeart, FaHeart } from 'react-icons/fa';
import { getUserNamebyUserId } from "../service/apiService";

// Componente para exibir os detalhes do livro
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
    <button 
      className={`favorite-button ${isFavorited ? 'favorited' : ''}`} 
      onClick={handleFavoriteToggle}
    >
      {/* Exibindo o ícone do coração e texto dinâmico */}
      {isFavorited ? (
        <>
          <FaHeart color="red" /> 
          <span>Desfavoritar</span>
        </>
      ) : (
        <>
          <FaRegHeart color="gray" />
          <span>Favoritar</span>
        </>
      )}
    </button>
  </div>
);

// Componente para exibir o resumo da IA
const AiReviewCard = ({ aiReview }) => (
  <div className="review-card ai-review">
    <h3>Resumo geral por IA</h3>
    <p>{aiReview}</p>
  </div>
);

// Componente para exibir a lista de reviews
const ReviewList = ({ reviews, userNames, userData, onDeleteReview }) => {
  const navigate = useNavigate();

  const handleEditReview = (reviewId) => {
    navigate(`/review/${reviewId}`);
  };

  const handleDeleteReview = async (reviewId) => {
    const confirmDelete = window.confirm("Tem certeza que deseja excluir este review?");
    if (confirmDelete) {
      try {
        await deleteReviewById(reviewId);
        onDeleteReview(reviewId);
      } catch (error) {
        console.error("Erro ao deletar review:", error);
      }
    }
  };

  return (
    <div className="review-list">
      <h2>Reviews dos usuários</h2>
      {reviews.length > 0 ? (
        <ul>
          {reviews.map((review) => (
            <li key={review.id} className="review-item">
              <h3>{review.review_title}</h3>
              <h4>Review feito por {userNames[review.user_id] || 'Carregando...'}</h4>
              <p><strong>Avaliação Geral:</strong> {review.overall_rating.toFixed(2)}</p>
              <p><strong>História:</strong> {review.story_rating}</p>
              <p><strong>Escrita:</strong> {review.style_rating}</p>
              <p><strong>Personagens:</strong> {review.character_rating}</p>
              <p><strong>Recomenda?</strong> {review.recommendation ? "Sim" : "Não"}</p>
              <p>{review.review}</p>

              {/* Botões Editar/Deletar apenas se o usuário for o autor */}
              {userData?.id === review.user_id && (
                <div className="review-actions">
                  <button className="edit-btn" onClick={() => handleEditReview(review.id)}>Editar</button>
                  <button className="delete-btn" onClick={() => handleDeleteReview(review.id)}>Deletar</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p>Este livro ainda não possui reviews.</p>
      )}
    </div>
  );
};

const BookPage = () => {
  const { bookId } = useParams();
  const [book, setBook] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [aiReview, setAiReview] = useState(null);
  const [isFavorited, setIsFavorited] = useState(false);
  const [loading, setLoading] = useState(true);
  const [userNames, setUserNames] = useState({});
  const { userData, error } = useUser();
  const navigate = useNavigate();
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

        // Carregar os nomes dos usuários
        const names = {};
        for (const review of reviewsData) {
          if (!names[review.user_id]) {
            const userName = await getUserNamebyUserId(review.user_id);
            names[review.user_id] = userName || 'Desconhecido';
          }
        }
        setUserNames(names);
      } catch (error) {
        console.error("Erro ao buscar detalhes do livro e reviews:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBookAndReviews();
  }, [bookId, userData]);

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

  const handleReviewClick = async (e, book ) => {
      e.stopPropagation();
      navigate(`/review/${book.google_id}`);
    };

  return (
    <div className="book-page">
      {book ? (
        <>
          <BookDetails
            book={book}
            isFavorited={isFavorited}
            handleFavoriteToggle={handleFavoriteToggle}
          />
          <button
            className="review-btn"
            onClick={(e) => handleReviewClick(e, book)}
          >
            Escrever Review
          </button>

          {/* Exibe o resumo da IA se existir */}
          {aiReview && <AiReviewCard aiReview={aiReview} />}

          {/* Passa os nomes dos usuários como prop */}
          <ReviewList reviews={reviews} userNames={userNames} />
        </>
      ) : (
        <p>Livro não encontrado.</p>
      )}
    </div>
  );
};

export default BookPage;
