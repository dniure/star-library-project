import React from 'react';
import './styles/globals.css';

function App() {
    return (
        <div className="min-h-screen bg-gray-50 font-inter">
            <div className="container mx-auto px-4 py-8">
                <h1 className="text-4xl font-playfair font-bold text-primary-900 mb-4">
                    STAR Library
                </h1>
                <p className="text-gray-600">
                    Welcome to your library dashboard. The application is set up successfully!
                </p>
                <div className="mt-8 p-6 glass rounded-2xl shadow-lg">
                    <h2 className="text-xl font-semibold mb-2">Setup Complete</h2>
                    <p className="text-gray-700">
                        Backend and frontend are ready for development. 
                        Next step: implement the database models and API endpoints.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default App;
