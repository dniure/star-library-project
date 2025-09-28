// frontend/src/pages/Home.jsx
import React, { useState } from "react";
import { useDashboard } from "../hooks/useDashboard";
import { Dashboard } from "../components/Dashboard";
import { BookGrid } from "../components/BookGrid";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import { Header } from "../components/ui/Header";
import { BookModal } from "../components/BookModal";

export const Home = () => {
    const { dashboardData, loading, error } = useDashboard(1);
    const [selectedBook, setSelectedBook] = useState(null);

    if (loading) {
        return (
        <div className="flex items-center justify-center min-h-screen">
            <LoadingSpinner />
        </div>
        );
    }

    if (error) {
        return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-red-600">Error loading dashboard: {error}</div>
        </div>
        );
    }

    if (!dashboardData) {
        return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-gray-600">No data available</div>
        </div>
        );
    }

    return (
        <div className="container mx-auto px-4 pt-20 pb-8">
            <Header userName="James" />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
            {/* Dashboard Container */}
            <div className="lg:col-span-1 glass no-hover p-6 rounded-xl">
                <Dashboard data={dashboardData} />
            </div>

            {/* Book Grid Container */}
            <div className="lg:col-span-2 glass no-hover p-6 rounded-xl">
                <BookGrid 
                books={dashboardData?.most_popular_books} 
                loading={loading}
                onBookClick={setSelectedBook}
                />
            </div>
            </div>

        {selectedBook && (
            <BookModal book={selectedBook} onClose={() => setSelectedBook(null)} />
        )}
        </div>
    );

};

