import React from 'react';

interface TodoSorterProps {
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  onSortChange: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
}

const TodoSorter: React.FC<TodoSorterProps> = ({ sortBy, sortOrder, onSortChange }) => {
  const handleSortChange = (newSortBy: string) => {
    // If clicking the same sort field, toggle the order
    if (sortBy === newSortBy) {
      const newOrder = sortOrder === 'asc' ? 'desc' : 'asc';
      onSortChange(newSortBy, newOrder);
    } else {
      // If clicking a different sort field, default to descending
      onSortChange(newSortBy, 'desc');
    }
  };

  return (
    <div className="mb-4 flex items-center">
      <span className="mr-2">Sort by:</span>
      <button
        onClick={() => handleSortChange('createdAt')}
        className={`mr-2 px-3 py-1 rounded ${
          sortBy === 'createdAt' ? 'bg-blue-500 text-white' : 'bg-gray-200'
        }`}
      >
        Created {sortBy === 'createdAt' && (sortOrder === 'asc' ? '↑' : '↓')}
      </button>
      <button
        onClick={() => handleSortChange('updatedAt')}
        className={`mr-2 px-3 py-1 rounded ${
          sortBy === 'updatedAt' ? 'bg-blue-500 text-white' : 'bg-gray-200'
        }`}
      >
        Updated {sortBy === 'updatedAt' && (sortOrder === 'asc' ? '↑' : '↓')}
      </button>
      <button
        onClick={() => handleSortChange('priority')}
        className={`px-3 py-1 rounded ${
          sortBy === 'priority' ? 'bg-blue-500 text-white' : 'bg-gray-200'
        }`}
      >
        Priority {sortBy === 'priority' && (sortOrder === 'asc' ? '↑' : '↓')}
      </button>
    </div>
  );
};

export default TodoSorter;