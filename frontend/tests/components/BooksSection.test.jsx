import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BookCard, BookGrid, BookModal } from '../src/components/BooksSection';
import { mockBook } from '../setup';

describe('BookCard', () => {
  const defaultProps = {
    book: mockBook,
    onClick: jest.fn(),
    className: 'test-class',
    style: { animationDelay: '0.1s' }
  };

  test('renders book information correctly', () => {
    render(<BookCard {...defaultProps} />);
    
    expect(screen.getByText('Test Book')).toBeInTheDocument();
    expect(screen.getByText('by Test Author')).toBeInTheDocument();
    expect(screen.getByText('🏷️ Fiction')).toBeInTheDocument();
    expect(screen.getByText('📖 300 pages')).toBeInTheDocument();
    expect(screen.getByText('📊 150 readers')).toBeInTheDocument();
    expect(screen.getByText('⏱️ 5h read')).toBeInTheDocument();
  });

  test('displays correct star rating', () => {
    render(<BookCard {...defaultProps} />);
    
    expect(screen.getByText('⭐⭐⭐⭐⭐')).toBeInTheDocument();
    expect(screen.getByText('(4.5)')).toBeInTheDocument();
  });

  test('handles missing author name', () => {
    const bookWithoutAuthor = { ...mockBook, author: null };
    render(<BookCard {...defaultProps} book={bookWithoutAuthor} />);
    
    expect(screen.getByText('by Unknown Author')).toBeInTheDocument();
  });

  test('calls onClick when card is clicked', () => {
    render(<BookCard {...defaultProps} />);
    
    const card = screen.getByText('Test Book').closest('.book-card');
    fireEvent.click(card);
    
    expect(defaultProps.onClick).toHaveBeenCalled();
  });
});

describe('BookGrid', () => {
  const defaultProps = {
    books: [mockBook],
    loading: false,
    onBookClick: jest.fn()
  };

  test('renders book grid with books', () => {
    render(<BookGrid {...defaultProps} />);
    
    expect(screen.getByText('Most Popular Books')).toBeInTheDocument();
    expect(screen.getByText('Test Book')).toBeInTheDocument();
  });

  test('shows loading state', () => {
    render(<BookGrid {...defaultProps} loading={true} />);
    
    const loadingSkeletons = document.querySelectorAll('.animate-pulse');
    expect(loadingSkeletons.length).toBeGreaterThan(0);
  });

  test('shows empty state when no books', () => {
    render(<BookGrid {...defaultProps} books={[]} />);
    
    expect(screen.getByText('No books available')).toBeInTheDocument();
  });
});

describe('BookModal', () => {
  const defaultProps = {
    book: mockBook,
    onClose: jest.fn()
  };

  test('renders book details in modal', () => {
    render(<BookModal {...defaultProps} />);
    
    expect(screen.getByText('Test Book')).toBeInTheDocument();
    expect(screen.getByText('by Test Author')).toBeInTheDocument();
    expect(screen.getByText('Test book description')).toBeInTheDocument();
    expect(screen.getByText('📖 300 pages')).toBeInTheDocument();
    expect(screen.getByText('🏷️ Fiction')).toBeInTheDocument();
    expect(screen.getByText('📅 Published: 2023')).toBeInTheDocument();
  });

  test('returns null when no book provided', () => {
    const { container } = render(<BookModal book={null} onClose={jest.fn()} />);
    
    expect(container.firstChild).toBeNull();
  });

  test('calls onClose when close button is clicked', () => {
    render(<BookModal {...defaultProps} />);
    
    const closeButton = screen.getByText('✖');
    fireEvent.click(closeButton);
    
    expect(defaultProps.onClose).toHaveBeenCalled();
  });
});