// src/components/ui/Skeleton.jsx
import React from "react";

export const Skeleton = ({ className }) => {
  return (
    <div className={`animate-pulse bg-gray-200 rounded-md ${className}`} />
  );
};
