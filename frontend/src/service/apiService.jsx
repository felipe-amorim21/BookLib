import axios from 'axios';


const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchBooks = async (query) => {
    try {
      const response = await axios.get('https://www.googleapis.com/books/v1/volumes', {
        params: {
          q: query, // Termo de pesquisa
          maxResults: 10, // Limite de resultados
        },
      });
      return response.data.items.map((item) => ({
        id: item.id,
        title: item.volumeInfo.title || 'Título Desconhecido',
        author: item.volumeInfo.authors ? item.volumeInfo.authors.join(', ') : 'Autor Desconhecido',
        description: item.volumeInfo.description || 'Sem descrição.',
        thumbnail: item.volumeInfo.imageLinks?.thumbnail || '', // Miniatura da capa
      }));
    } catch (error) {
      console.error('Erro ao buscar livros:', error);
      return [];
    }
  };

// Funções CRUD de Books

export const getBooks = async () => {
  const response = await api.get('/books/');
  return response.data;
};

export const getBookById = async (id) => {
  const response = await api.get(`/books/${id}`);
  return response.data;
};

export const createBook = async (bookData) => {
  const response = await api.post('/books/', bookData);
  return response.data;
};

export const updateBook = async (id, bookData) => {
  const response = await api.put(`/books/${id}`, bookData);
  return response.data;
};

export const deleteBook = async (id) => {
  const response = await api.delete(`/books/${id}`);
  return response.data;
};

// Funções CRUD de Reviews

export const getReviewsByBookId = async (bookId) => {
  const response = await api.get(`/books/${bookId}/reviews`);
  return response.data;
};

export const createReview = async (bookId, reviewData) => {
  const response = await api.post(`/books/${bookId}/reviews`, reviewData);
  return response.data;
};

export const updateReview = async (bookId, reviewId, reviewData) => {
  const response = await api.put(`/books/${bookId}/reviews/${reviewId}`, reviewData);
  return response.data;
};

export const deleteReview = async (bookId, reviewId) => {
  const response = await api.delete(`/books/${bookId}/reviews/${reviewId}`);
  return response.data;
};
