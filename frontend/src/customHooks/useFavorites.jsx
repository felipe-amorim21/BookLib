import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const API_BASE_URL = "http://localhost:8000/api/v1";

export function useFavorites() {
  console.log(useAuth);
  const { authToken } = useAuth();
  const [favorites, setFavorites] = useState(new Set());

  useEffect(() => {
    if (authToken) {
      fetch(`${API_BASE_URL}/favoritos`, {
        headers: { Authorization: `Bearer ${authToken}` },
      })
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data)) {
            setFavorites(new Set(data.map((book) => book.id)));
          }
        })
        .catch((err) => console.error("Erro ao buscar favoritos:", err));
    }
  }, [authToken]);

  const toggleFavorite = async (bookId) => {
    const isFavorited = favorites.has(bookId);
    const url = `${API_BASE_URL}/${isFavorited ? "desfavoritar" : "favoritar"}/${bookId}`;
    const method = isFavorited ? "DELETE" : "POST";

    try {
      const response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) throw new Error("Erro ao atualizar favorito");

      setFavorites((prevFavorites) => {
        const newFavorites = new Set(prevFavorites);
        if (isFavorited) newFavorites.delete(bookId);
        else newFavorites.add(bookId);
        return newFavorites;
      });
    } catch (error) {
      console.error("Erro ao favoritar/desfavoritar:", error);
    }
  };

  return { favorites, toggleFavorite };
}
