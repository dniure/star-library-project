// src/components/ui/Button.jsx
import React from "react";

export const Button = ({ children, onClick, variant = "primary" }) => {
  const base =
    "px-4 py-2 rounded-lg font-semibold transition-colors focus:outline-none";
  const variants = {
    primary: "bg-[#1a237e] text-white hover:bg-[#0d174a]",
    secondary: "bg-[#2e7d32] text-white hover:bg-[#1e5d23]",
    accent: "bg-[#ffd700] text-black hover:bg-[#e6c200]",
  };

  return (
    <button onClick={onClick} className={`${base} ${variants[variant]}`}>
      {children}
    </button>
  );
};
