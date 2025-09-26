// src/components/ui/Card.jsx
import React from 'react';

export const Card = ({ children, className = '', hover = false, ...props }) => {
    return (
        <div 
            className={`bg-white/85 backdrop-blur-lg rounded-2xl border border-white/20 shadow-lg 
                       ${hover ? 'transition-transform hover:scale-105 hover:shadow-xl' : ''} 
                       ${className}`}
            {...props}
        >
            {children}
        </div>
    );
};