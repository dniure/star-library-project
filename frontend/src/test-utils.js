// src/test-utils.js
import React from 'react';
import { render } from '@testing-library/react';
import { AppProvider } from './context/AppContext';

// Mock data that matches your actual API schema
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

export const mockUser = {
  id: 1,
  name: "Test User",
  favoriteGenre: "Fantasy"
};

// Custom render with providers
export const renderWithProviders = (ui, options = {}) => {
  return render(ui, {
    wrapper: ({ children }) => (
      <AppProvider>
        {children}
      </AppProvider>
    ),
    ...options,
  });
};

// Re-export everything from testing-library
export * from '@testing-library/react';