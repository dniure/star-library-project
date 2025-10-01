// tests/setup.js
require('@testing-library/jest-dom');

// Mock data only - remove the API mock from here
const mockBook = {
  id: 1,
  title: 'Test Book',
  author: { name: 'Test Author', id: 1, bio: 'Test bio' },
  genre: 'Fiction',
  pages: 300,
  published_year: 2023,
  readers_count: 150,
  reading_time: 5,
  cover_image_url: '/test-cover.jpg',
  rating: 4.5,
  description: 'Test book description'
};

const mockDashboardData = {
  reader_id: 1,
  reader_name: 'John Doe',
  most_popular_books: [mockBook],
  most_popular_author: {
    id: 1,
    name: 'Popular Author',
    bio: 'Best selling author',
    books_count: 10,
    total_readers: 5000
  },
  user_books_read: [mockBook],
  user_top_authors: [
    { id: 1, name: 'Author 1', books_count: 5 },
    { id: 2, name: 'Author 2', books_count: 3 }
  ]
};

// Custom render with providers
const customRender = (ui, { providerProps, ...renderOptions } = {}) => {
  const { render } = require('@testing-library/react');
  return render(ui, { ...renderOptions });
};

module.exports = {
  mockBook,
  mockDashboardData,
  render: customRender
};