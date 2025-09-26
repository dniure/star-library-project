// src/components/ui/Header.jsx
import React from "react";

export const Header = ({ userName = "Emily" }) => {
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
