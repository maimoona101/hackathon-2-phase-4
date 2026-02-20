'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../lib/auth';
import TodoItem from '../../components/todos/TodoItem';
import CreateTodoForm from '../../components/todos/CreateTodoForm';
import TodoFilter from '../../components/todos/TodoFilter';
import TodoSorter from '../../components/todos/TodoSorter';
import { Todo } from '../../types/todo';
import { apiClient } from '../../lib/api';

const TodoPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('createdAt');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    if (isAuthenticated) {
      fetchTodos();
    }
  }, [isAuthenticated]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data: Todo[] = await apiClient.getTodos(); // TS ke liye type define
      setTodos(data);
    } catch (error: any) {
      console.error('Failed to fetch todos:', error);
      alert('Failed to fetch todos: ' + (error?.message || error));
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (title: string, description?: string, priority: string = 'medium') => {
    try {
      const newTodo: Todo = await apiClient.createTodo(title, description, priority);
      setTodos([newTodo, ...todos]);
    } catch (error: any) {
      console.error('Failed to create todo:', error);
      alert('Failed to create todo: ' + (error?.message || error));
    }
  };

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    const originalTodo = todos.find(todo => todo.id === id);
    setTodos(prev => prev.map(todo => (todo.id === id ? { ...todo, ...updates } : todo)));

    try {
      const updatedTodo: Todo = await apiClient.updateTodo(id, updates);
      setTodos(prev => prev.map(todo => (todo.id === id ? updatedTodo : todo)));
    } catch (error: any) {
      console.error('Failed to update todo:', error);
      if (originalTodo) setTodos(prev => prev.map(todo => (todo.id === id ? originalTodo : todo)));
      alert('Failed to update todo: ' + (error?.message || error));
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      await apiClient.deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (error: any) {
      console.error('Failed to delete todo:', error);
      alert('Failed to delete todo: ' + (error?.message || error));
    }
  };

  const filteredAndSortedTodos = React.useMemo(() => {
    let filtered = [...todos];
    if (statusFilter === 'completed') filtered = filtered.filter(t => t.status === 'completed');
    else if (statusFilter === 'pending') filtered = filtered.filter(t => t.status === 'pending');

    filtered.sort((a, b) => {
      const dir = sortOrder === 'asc' ? 1 : -1;
      if (sortBy === 'created_at') return dir * (new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
      return 0;
    });

    return filtered;
  }, [todos, statusFilter, sortBy, sortOrder]);

  if (!isAuthenticated) return <div>Please log in to access your todos.</div>;
  if (loading) return <div>Loading todos...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">My Todos</h1>

      <CreateTodoForm onCreate={handleCreateTodo} />

      <div className="mb-6">
        <TodoFilter status={statusFilter} onStatusChange={setStatusFilter} />
        <TodoSorter
          sortBy={sortBy}
          sortOrder={sortOrder}
          onSortChange={(newSortBy: string, newSortOrder: 'asc' | 'desc') => {
            setSortBy(newSortBy);
            setSortOrder(newSortOrder);
          }}
        />
      </div>

      <div>
        {filteredAndSortedTodos.length === 0 ? (
          <p className="text-gray-500">No todos found. Create one above!</p>
        ) : (
          filteredAndSortedTodos.map(todo => (
            <TodoItem key={todo.id} todo={todo} onUpdate={handleUpdateTodo} onDelete={handleDeleteTodo} />
          ))
        )}
      </div>
    </div>
  );
};

export default TodoPage;
