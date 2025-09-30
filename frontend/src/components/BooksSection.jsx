/**
 * BooksSection.jsx
 * ----------------
 * Contains all book-related components:
 * - BookCard: Display single book
 * - BookGrid: Display grid of books
 * - BookModal: Show detailed book info
 */

// Book Card Component
export const BookCard = ({ book, onClick, className, style }) => {
    const stars = '⭐'.repeat(Math.round(book.rating || 4));

    return (
        <div
            onClick={onClick}
            className={`book-card glass rounded-2xl shadow-lg p-4 flex flex-col cursor-pointer ${className}`}
            style={style}
        >
            <div className="mb-3 w-full h-48 overflow-hidden rounded-xl">
                <img src={book.cover_image_url || '/assets/cover_placeholder.jpg'} alt={book.title} className="w-full h-full object-cover" />
            </div>

            <div className="flex items-center justify-start mb-2 space-x-2 text-yellow-500 font-medium">
                <span>{stars}</span>
                <span className="text-gray-600 text-sm">({book.rating?.toFixed(1) || 4})</span>
            </div>

            <hr className="border-gray-200 mb-2" />
            <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">{book.title}</h3>
            <p className="text-sm text-gray-500 mb-3">by {book.author?.name || "Unknown Author"}</p>

            <div className="flex justify-between text-xs text-gray-500 mb-3">
                <span>📊 {book.readers_count} readers</span>
                <span>📖 {book.pages} pages</span>
            </div>
            <div className="flex justify-between text-xs text-gray-500 mb-3">
                <span>🏷️ {book.genre}</span>
                <span>⏱️ {book.reading_time}h read</span>
            </div>

            <div className="flex gap-2 mt-auto">
                <button className="flex-1 bg-blue-700 text-white py-1 rounded-lg hover:bg-blue-800 text-sm" onClick={e => e.stopPropagation()}>
                    Add to Library
                </button>
                <button className="flex-1 border border-blue-700 text-blue-700 py-1 rounded-lg hover:bg-blue-100 text-sm" onClick={e => { e.stopPropagation(); onClick(book); }}>
                    Quick Preview
                </button>
            </div>
        </div>
    );
};


// Book Grid Component
export const BookGrid = ({ books, loading, onBookClick }) => {
    if (loading) return (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {[...Array(6)].map((_, idx) => <div key={idx} className="animate-pulse bg-gray-200 h-48 w-full rounded-xl" />)}
        </div>
    );

    if (!books || books.length === 0) return <div className="text-center py-8"><p className="text-gray-500">No books available</p></div>;

    return (
        <div>
            <h2 className="text-2xl font-bold text-[#1a237e] mb-6 font-playfair">Most Popular Books</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {books.map((book, idx) => (
                    <BookCard key={book.id} book={book} onClick={() => onBookClick(book)} className="fade-in-up" style={{ animationDelay: `${idx * 0.1}s` }} />
                ))}
            </div>
        </div>
    );
};


// Book Modal Component
export const BookModal = ({ book, onClose }) => {
    if (!book) return null;

    return (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/50">
            <div className="glass p-6 rounded-2xl max-w-lg w-full relative fade-in">
                <button onClick={onClose} className="absolute top-3 right-3 text-gray-500 hover:text-gray-700">✖</button>
                <h2 className="text-2xl font-bold text-[#1a237e] mb-2 font-playfair">{book.title}</h2>
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
