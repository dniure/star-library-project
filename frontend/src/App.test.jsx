// src/App.test.jsx
import { render, screen, act } from '@testing-library/react';
import App from './App';

// Mock the API service
jest.mock('./services/api', () => ({
  apiService: {
    fetchDashboardData: jest.fn().mockResolvedValue({
      reader_id: 1,
      reader_name: "Test User",
      most_popular_books: [],
      user_books_read: [],
      user_top_authors: []
    })
  }
}));

test('renders app without crashing', async () => {
  await act(async () => {
    render(<App />);
  });
  
  // The app might show different states - check that it renders something meaningful
  // Look for any of these possible states
  const possibleTexts = [
    'Loading...',
    'No data available', 
    'Reading Dashboard',
    'Most Popular Books'
  ];
  
  const foundText = possibleTexts.find(text => 
    screen.queryByText(text) !== null
  );
  
  // The test passes if any expected text is found (app didn't crash)
  expect(foundText).toBeTruthy();
});