// frontend/src/components/BookGrid.jsx
import React from 'react';
import { BookCard } from './BookCard';

export const BookGrid = ({ books }) => {
    if (!books || books.length === 0) {
        return (
            <div className="text-center py-8">
                <p className="text-gray-500">No books available</p>
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Most Popular Books</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {books.map((book) => (
                    <BookCard key={book.id} book={book} />
                ))}                
            </div>
        </div>
    );
};

export default BookGrid;