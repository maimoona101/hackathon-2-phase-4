import React from 'react';

interface TodoSearchProps {
  searchTerm: string;
  onSearchChange: (searchTerm: string) => void;
}

const TodoSearch: React.FC<TodoSearchProps> = ({ searchTerm, onSearchChange }) => {
  return (
    <div className="mb-4">
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
        placeholder="Search todos..."
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
};

export default TodoSearch;