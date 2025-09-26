// frontend/src/components/BookModal.jsx
import React from 'react';

export const BookModal = ({ book, onClose }) => {
    if (!book) return null;

    return (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/50">
            <div className="glass p-6 rounded-2xl max-w-lg w-full relative fade-in">
                <button 
                    onClick={onClose}
                    className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
                >
                    ✖
                </button>
                <h2 className="text-2xl font-bold text-[#1a237e] mb-2 font-playfair">
                    {book.title}
                </h2>
                <p className="text-gray-600 mb-4">by {book.author?.name}</p>
                <p className="text-sm text-gray-700 mb-4">{book.description}</p>
                <div className="text-sm text-gray-500 space-y-1">
                    <p>📖 {book.pages} pages</p>
                    <p>🏷️ {book.genre}</p>
                    <p>📅 Published: {book.published_year}</p>
                </div>
            </div>
        </div>
    );
};
