import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Função para buscar livros da API do Google
export const searchBooks = async (query) => {
    try {
      const response = await axios.get('https://www.googleapis.com/books/v1/volumes', {
        params: {
          q: query, 
          maxResults: 10, 
        },
      });
      return response.data.items.map((item) => ({
        id: item.id,
        title: item.volumeInfo.title || 'Título Desconhecido',
        author: item.volumeInfo.authors ? item.volumeInfo.authors.join(', ') : 'Autor Desconhecido',
        description: item.volumeInfo.description || 'Sem descrição.',
        thumbnail: item.volumeInfo.imageLinks?.thumbnail || '', 

        published_year: item.volumeInfo.publishedDate ? parseInt(item.volumeInfo.publishedDate.split('-')[0]) : null,
        genre: item.volumeInfo.categories ? item.volumeInfo.categories[0] : '',
      }));
    } catch (error) {
      console.error('Erro ao buscar livros:', error);
      return [];
    }
  };
  
  export const saveBookIfNotExist = async (book) => {
    console.log("livro: ", book);
    try {
      console.log("Verificando se o livro já existe...");
      const response = await api.get(`/books/google/${book.id}`);
      console.log("Resposta da verificação:", response.data);

      if (!response.data) {
        
        const bookData = {
          title: book.title,
          author: book.author,
          description: book.description,
          genre: book.genre || '', 
          published_year: book.published_year || null, 
        };

        console.log("Chegou na criação do livro");
  
        await createBook(bookData);
      } else {
        console.log("O livro já existe no backend.");
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        console.log("Livro não encontrado. Criando novo livro...");
        
        const bookData = {
          title: book.title,
          author: book.author,
          google_id: book.id,
          description: book.description,
          genre: book.genre || '', 
          published_year: book.published_year || null, 
        };

        console.log("Criando o livro...");
        console.log(bookData)
        await createBook(bookData);
      } else {
        console.error('Erro ao salvar o livro:', error);
      }
    }
};



  

// Função para salvar uma review
export const saveReview = async (bookId, review) => {
  try {
    await api.post('/api/reviews', { bookId, review });
  } catch (error) {
    console.error('Erro ao salvar a review:', error);
  }
};

// Funções CRUD de Books

export const getBooks = async () => {
  try {
    const response = await api.get('/books/');
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar livros:', error);
    return [];
  }
};

export const getBookById = async (id) => {
  try {
    const response = await api.get(`/books/${id}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar o livro:', error);
    return null;
  }
};

export const getBookByGoogleId = async (id) => {
    try {
      const response = await api.get(`/books/google/${id}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar o livro:', error);
      return null;
    }
  };

export const createBook = async (bookData) => {
  try {
    const response = await api.post('/books/', bookData);
    return response.data;
  } catch (error) {
    console.error('Erro ao criar livro:', error);
    return null;
  }
};

export const updateBook = async (id, bookData) => {
  try {
    const response = await api.put(`/books/${id}`, bookData);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar livro:', error);
    return null;
  }
};

export const deleteBook = async (id) => {
  try {
    const response = await api.delete(`/books/${id}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar livro:', error);
    return null;
  }
};

// Funções CRUD de Reviews

export const getReviewsByBookId = async (bookId) => {
  try {
    const response = await api.get(`/reviews/books/${bookId}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar reviews:', error);
    return [];
  }
};

export const createReview = async (reviewData) => {
  try {
    const response = await api.post(`/reviews`, reviewData);
    return response.data;
  } catch (error) {
    console.error('Erro ao criar review:', error);
    return null;
  }
};

export const updateReview = async (bookId, reviewId, reviewData) => {
  try {
    const response = await api.put(`/books/${bookId}/reviews/${reviewId}`, reviewData);
    return response.data;
  } catch (error) {
    console.error('Erro ao atualizar review:', error);
    return null;
  }
};

export const deleteReview = async (bookId, reviewId) => {
  try {
    const response = await api.delete(`/books/${bookId}/reviews/${reviewId}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar review:', error);
    return null;
  }
};
