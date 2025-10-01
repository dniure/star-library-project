// src/__mocks__/api.js
export const mockBook = {
  id: 1,
  title: "Test Book",
  description: "Test description",
  genre: "Fantasy",
  pages: 320,
  published_year: 2020,
  author: {
    id: 1,
    name: "Test Author",
    bio: "Test bio",
    nationality: "British",
    books_count: 5,
    total_readers: 1000
  },
  readers_count: 100,
  reading_time: 5,
  cover_image_url: "/test-cover.jpg",
  rating: 4.5
};

export const mockAuthor = {
  id: 1,
  name: "Test Author",
  bio: "Test bio",
  nationality: "British",
  books_count: 5,
  total_readers: 1000
};

export const mockDashboardData = {
  reader_id: 1,
  reader_name: "Test User",
  most_popular_books: [mockBook],
  most_popular_author: mockAuthor,
  user_books_read: [mockBook],
  user_top_authors: [mockAuthor]
};

// Mock the API service
export const apiService = {
  fetchDashboardData: jest.fn().mockResolvedValue(mockDashboardData),
  fetchBooks: jest.fn().mockResolvedValue([mockBook]),
  fetchAuthors: jest.fn().mockResolvedValue([mockAuthor]),
  fetchReader: jest.fn().mockResolvedValue({
    id: 1,
    name: "Test User",
    email: "test@example.com",
    join_date: "2023-01-01",
    favorite_genre: "Fantasy",
    books_read_count: 1
  })
};

export class ApiError extends Error {
  constructor(message, status, originalError) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.originalError = originalError;
  }
}

export default apiService;