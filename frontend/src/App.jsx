// src/App.jsx
import React from 'react';
import { Home } from './pages/Home';
import { AppProvider } from './context/AppContext';
import './styles/globals.css';

function App() {
    return (
        <AppProvider>
            <div className="min-h-screen bg-gray-50">
                <Home />
            </div>
        </AppProvider>
    );
}

export default App;