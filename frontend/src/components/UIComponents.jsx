// UI Compontents
import { useEffect, useState } from "react";

// Header
export const Header = ({ userName }) => {
  return (
    <header className="fixed top-0 left-0 right-0 w-full z-50 bg-[#090f52] h-16 flex justify-between items-center px-8 shadow-md">
      {/* Logo */}
      <div className="text-2xl font-bold text-[#ffd700] font-playfair">
        STAR Library
      </div>

      {/* User welcome */}
      <div className="text-white pr-4">
        Welcome, {userName}! 👋
      </div>
    </header>
  );
};

// Generic Card
export const Card = ({ children, className = '', hover = false, ...props }) => (
    <div 
        className={`bg-white/85 backdrop-blur-lg rounded-2xl border border-white/20 shadow-lg 
                   ${hover ? 'transition-transform hover:scale-105 hover:shadow-xl' : ''} 
                   ${className}`}
        {...props}
    >
        {children}
    </div>
);

// StatCard
export const StatCard = ({ title, icon, children, className = '' }) => (
    <div className={`bg-white/85 backdrop-blur-lg rounded-2xl border border-white/20 shadow-lg p-6 ${className}`}>
        <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">{icon}</span>
            <h3 className="font-semibold text-gray-900">{title}</h3>
        </div>
        {children}
    </div>
);

// Loading Spinner
export const LoadingSpinner = ({ message = "Loading..." }) => (
    <div className="flex flex-col items-center justify-center p-8">
        <div className="spinner"></div>
        <p className="mt-4 text-gray-600">{message}</p>
    </div>
);

// Animated stat number
export const StatNumber = ({ value, duration = 1000 }) => {
    const [count, setCount] = useState(0);

    useEffect(() => {
        let start = 0;
        const stepTime = Math.abs(Math.floor(duration / value));
        const timer = setInterval(() => {
            start += 1;
            setCount(start);
            if (start >= value) clearInterval(timer);
        }, stepTime);
        return () => clearInterval(timer);
    }, [value, duration]);

    return <span className="font-semibold text-green-600">{count}</span>;
};
