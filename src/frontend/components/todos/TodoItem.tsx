import React from "react";
import { Todo } from "../../types/todo";

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: string, updates: Partial<Todo>) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onUpdate, onDelete }) => {
  const handleToggleStatus = (e: React.ChangeEvent<HTMLInputElement>) => {
    onUpdate(todo.id, {
      status: e.target.checked ? "completed" : "pending",
    });
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onUpdate(todo.id, {
      priority: e.target.value as "low" | "medium" | "high",
    });
  };

  return (
    <div
      className={`border rounded-lg p-4 mb-2 flex items-center justify-between ${
        todo.status === "completed" ? "bg-green-50" : "bg-white"
      }`}
    >
      <div className="flex items-center">
        {/* ✅ CONTROLLED CHECKBOX */}
        <input
          type="checkbox"
          checked={todo.status === "completed"}
          onChange={handleToggleStatus}
          className="mr-3 h-5 w-5"
        />
        <div>
          <h3
            className={`font-medium ${
              todo.status === "completed"
                ? "line-through text-gray-500"
                : "text-gray-800"
            }`}
          >
            {todo.title}
          </h3>
          {todo.description && (
            <p className="text-sm text-gray-600 mt-1">{todo.description}</p>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <select
          value={todo.priority}
          onChange={handlePriorityChange}
          className={`px-2 py-1 rounded text-sm ${
            todo.priority === "high"
              ? "bg-red-100 text-red-800"
              : todo.priority === "medium"
              ? "bg-yellow-100 text-yellow-800"
              : "bg-green-100 text-green-800"
          }`}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>

        <button
          onClick={handleDelete}
          className="text-red-500 hover:text-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TodoItem;
