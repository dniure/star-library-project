// frontend/src/pages/Home.jsx
import React from 'react';
import { useDashboard } from '../hooks/useDashboard';
import { Dashboard } from '../components/Dashboard';
import { BookGrid } from '../components/BookGrid';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';

export const Home = () => {
    const { dashboardData, loading, error } = useDashboard(1); // Reader ID 1

    React.useEffect(() => {
        if (dashboardData) {
            console.log('Dashboard Data:', dashboardData);
            if (dashboardData.most_popular_books) {
                console.log('First book structure:', dashboardData.most_popular_books[0]);
                console.log('First book author type:', typeof dashboardData.most_popular_books[0]?.author);
                console.log('First book author:', dashboardData.most_popular_books[0]?.author);
            }
        }
    }, [dashboardData]);

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
        <div className="container mx-auto px-4 py-8">
            {/* Header */}
            <header className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-2">
                    STAR Library
                </h1>
                <p className="text-gray-600">Welcome to your reading dashboard</p>
            </header>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Dashboard Sidebar */}
                <div className="lg:col-span-1">
                    <Dashboard data={dashboardData} />
                </div>

                {/* Book Grid */}
                <div className="lg:col-span-2">
                    <BookGrid books={dashboardData.most_popular_books} />
                </div>
            </div>
        </div>
    );
};