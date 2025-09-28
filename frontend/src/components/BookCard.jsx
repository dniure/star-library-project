// frontend/src/components/BookCard.jsx

export const BookCard = ({ book, onClick, className, style }) => {
    const stars = '⭐'.repeat(Math.round(book.rating || 4));
    // console.log("book: ", book)
    return (
        <div
            onClick={onClick}
            className={`book-card glass rounded-2xl shadow-lg p-4 flex flex-col cursor-pointer ${className}`}
            style={style}
        >
            {/* Book Cover */}
            <div className="mb-3 w-full h-48 overflow-hidden rounded-xl">
                <img 
                    src={book.cover_image_url || '/assets/cover_placeholder.jpg'} 
                    alt={book.title} 
                    className="w-full h-full object-cover"
                />
            </div>

            {/* Rating */}
            <div className="flex items-center justify-start mb-2 space-x-2 text-yellow-500 font-medium">
                <span>{stars}</span>
                <span className="text-gray-600 text-sm">({book.rating?.toFixed(1) || 4})</span>
            </div>

            <hr className="border-gray-200 mb-2" />

            {/* Title & Author */}
            <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">{book.title}</h3>
            <p className="text-sm text-gray-500 mb-3">by {book.author?.name || "Unknown Author"}</p>

            {/* Book Stats */}
            <div className="flex justify-between text-xs text-gray-500 mb-3">
                <span>📊 {book.readers_count} readers</span>
                <span>📖 {book.pages} pages</span>
            </div>
            <div className="flex justify-between text-xs text-gray-500 mb-3">
                <span>🏷️ {book.genre}</span>
                <span>⏱️ {book.reading_time}h read</span>
            </div>

            {/* Buttons */}
            <div className="flex gap-2 mt-auto">
                <button 
                    className="flex-1 bg-blue-700 text-white py-1 rounded-lg hover:bg-blue-800 text-sm"
                    onClick={(e) => { e.stopPropagation()}}
                >
                    Add to Library
                </button>
                <button 
                    className="flex-1 border border-blue-700 text-blue-700 py-1 rounded-lg hover:bg-blue-100 text-sm"
                    onClick={(e) => { e.stopPropagation(); onClick(book); }}
                >
                    Quick Preview
                </button>
            </div>
        </div>
    );
};
