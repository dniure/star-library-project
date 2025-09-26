// frontend/src/components/ui/LoadingSpinner.jsx
import React from 'react';

export const LoadingSpinner = ({ message = "Loading..." }) => {
    return (
        <div className="flex flex-col items-center justify-center p-8">
            <div className="spinner"></div>
            <p className="mt-4 text-gray-600">{message}</p>
        </div>
    );
};

export default LoadingSpinner;