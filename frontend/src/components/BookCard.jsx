// frontend/src/components/BookCard.jsx
import React from 'react';

export const BookCard = ({ book }) => {
    // Safely access author name - handle both object and string cases
    const getAuthorName = () => {
        if (!book.author) return "Unknown Author";
        if (typeof book.author === 'string') return book.author;
        return book.author.name || "Unknown Author";
    };

    const stars = '⭐'.repeat(Math.round(book.rating || 4));
    
    return (
        <div className="bg-white/85 backdrop-blur-lg rounded-2xl border border-white/20 shadow-lg p-4 h-full flex flex-col transition-transform hover:scale-105 hover:shadow-xl">
            <div className="flex items-start justify-between mb-3">
                <span className="text-yellow-500 text-sm">{stars}</span>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                    {book.readers_count || 0} readers
                </span>
            </div>
            
            <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                {book.title || "Untitled Book"}
            </h3>
            
            <p className="text-sm text-gray-600 mb-3">by {getAuthorName()}</p>
            
            <div className="mt-auto space-y-2">
                <div className="flex justify-between text-xs text-gray-500">
                    <span>📖 {book.pages || 'N/A'} pages</span>
                    <span>🏷️ {book.genre || 'Unknown'}</span>
                </div>
            </div>
        </div>
    );
};

export default BookCard;