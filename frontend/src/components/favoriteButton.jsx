import { useFavorites } from "../hooks/useFavorites";
import { Heart, HeartFill } from "lucide-react"; // Instale a biblioteca se necessário

const FavoriteButton = ({ bookId }) => {
  const { favorites, toggleFavorite } = useFavorites();
  const isFavorited = favorites.has(bookId);

  return (
    <button onClick={() => toggleFavorite(bookId)} className="p-2">
      {isFavorited ? <HeartFill className="text-red-500" /> : <Heart className="text-gray-500" />}
    </button>
  );
};

export default FavoriteButton;