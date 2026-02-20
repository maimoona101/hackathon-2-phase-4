import React from 'react';

interface TodoFilterProps {
  status: string;
  onStatusChange: (status: string) => void;
}

const TodoFilter: React.FC<TodoFilterProps> = ({ status, onStatusChange }) => {
  return (
    <div className="mb-4">
      <span className="mr-4">Filter:</span>
      <button
        onClick={() => onStatusChange('all')}
        className={`mr-2 px-3 py-1 rounded ${
          status === 'all' ? 'bg-blue-500 text-white' : 'bg-gray-200'
        }`}
      >
        All
      </button>
      <button
        onClick={() => onStatusChange('pending')}
        className={`mr-2 px-3 py-1 rounded ${
          status === 'pending' ? 'bg-blue-500 text-white' : 'bg-gray-200'
        }`}
      >
        Pending
      </button>
      <button
        onClick={() => onStatusChange('completed')}
        className={`px-3 py-1 rounded ${
          status === 'completed' ? 'bg-blue-500 text-white' : 'bg-gray-200'
        }`}
      >
        Completed
      </button>
    </div>
  );
};

export default TodoFilter;