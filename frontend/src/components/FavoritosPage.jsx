import React, { useEffect, useState } from 'react';
import { favoritesUser } from '../service/apiService';
import { useUser } from '../context/userContext';
import { useNavigate } from 'react-router-dom';

const FavoritosPage = () => {
    const { userData} = useUser();
    const [favoritos, setFavoritos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    console.log("userData favorito", userData)

    useEffect(() => {
        if (!userData) {
            return;
        }

        const fetchFavoritos = async () => {
            try {
                // Chama a função favoritesUser para buscar os favoritos
                console.log("aqui")
                const livrosFavoritos = await favoritesUser(userData);
                console.log("livros1: ", livrosFavoritos)
                if (livrosFavoritos) {
                    setFavoritos(livrosFavoritos);
                    console.log("livros: ", favoritos)
                } else {
                    setError('Nenhum favorito encontrado.');
                }
            } catch (err) {
                setError('Erro ao carregar os favoritos');
            } finally {
                setLoading(false);
            }
        };

        fetchFavoritos();
    }, [userData]);


    if (loading) {
        return <div>Carregando...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    const handleBookClick = async (book) => {
        navigate(`/book/${book.google_id}`);
      };

    return (
        <div>
            <h1>Livros Favoritos</h1>
            {favoritos.length === 0 ? (
                <p>Você ainda não favoritou nenhum livro.</p>
            ) : (
                <div className="books-list">
                    <div className="books-grid">
                        {favoritos.map((livro) => (
                            <div
                                key={livro.id}
                                className="book-item"
                                onClick={() => handleBookClick(livro)}
                            >
                                <h3 className="book-title">{livro.title}</h3>
                                <p className="book-author">
                                    <strong>Autor:</strong> {livro.author}
                                </p>
                                {livro.thumbnail && (
                                    <img
                                        src={livro.thumbnail}
                                        alt={livro.title}
                                        className="book-thumbnail"
                                    />
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default FavoritosPage;
