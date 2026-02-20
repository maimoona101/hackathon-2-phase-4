"use client";

import React from "react";
import { useAuth } from "../../lib/auth";
import AIChat from "../../components/AIChat";
import Link from "next/link";

const ChatPage = () => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Please log in to access the AI chat
          </h2>
          <Link
            href="/login"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
          >
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Task Assistant</h1>
        <p className="text-gray-600">
          Manage your tasks using natural language. Tell me to add, update, complete, or delete tasks.
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="h-[600px] flex flex-col">
          <AIChat userId={user?.id} />
        </div>
      </div>

      <div className="mt-6 text-center">
        <Link
          href="/todos"
          className="text-blue-600 hover:underline"
        >
          ← Back to My Todos
        </Link>
      </div>
    </div>
  );
};

export default ChatPage;