// frontend/src/components/BookGrid.jsx
import React from 'react';
import { BookCard } from './BookCard';

export const BookGrid = ({ books, loading, onBookClick }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {[...Array(6)].map((_, idx) => (
        <div key={idx} className="animate-pulse bg-gray-200 h-48 w-full rounded-xl" />
        ))}
      </div>
    );
  }

  if (!books || books.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No books available</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-[#1a237e] mb-6 font-playfair">
        Most Popular Books
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {books.map((book, idx) => (
          <BookCard
            key={book.id}
            book={book}
            onClick={() => onBookClick(book)}
            className="fade-in-up"
            style={{ animationDelay: `${idx * 0.1}s` }}
          />
        ))}
      </div>
    </div>
  );
};
