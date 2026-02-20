"use client";

import React from "react";
import { useAuth } from "../lib/auth";
import Link from "next/link";

const HomePage = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-900 to-gray-200 py-16">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white">
            Todo Web Application
          </h1>
          <p className="mt-6 max-w-2xl mx-auto text-lg sm:text-xl text-yellow-200">
            A secure, modern, and simple way to manage your daily tasks
            efficiently.
          </p>
        </div>

        {/* Main Card */}
        <div className="max-w-3xl mx-auto">
          {isAuthenticated ? (
            <div className="bg-white rounded-2xl shadow-xl p-10 border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Welcome 👋
              </h2>
              <p className="text-gray-600 mb-6">
                {user?.display_name || user?.email}, you are logged in
                successfully.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Link
                  href="/todos"
                  className="bg-blue-600 text-white py-3 px-6 rounded-xl text-center font-semibold hover:bg-blue-700 transition"
                >
                  View My Todos
                </Link>

                <Link
                  href="/profile"
                  className="bg-gray-100 text-gray-800 py-3 px-6 rounded-xl text-center font-semibold hover:bg-gray-200 transition"
                >
                  Profile
                </Link>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl shadow-xl p-10 border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                Get Started 🚀
              </h2>
              <p className="text-gray-600 mb-8">
                Sign in or create an account to start managing your todos
                securely.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Link
                  href="/login"
                  className="bg-blue-600 text-white py-3 px-6 rounded-xl text-center font-semibold hover:bg-blue-700 transition"
                >
                  Sign In
                </Link>

                <Link
                  href="/register"
                  className="bg-white text-blue-600 py-3 px-6 rounded-xl text-center font-semibold border-2 border-blue-600 hover:bg-blue-50 transition"
                >
                  Create Account
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* Footer Text */}
        <p className="text-center text-sm text-blue-900 mt-16">
          Built with Next.js, Tailwind CSS & Neon Database
        </p>
      </div>
    </div>
  );
};

export default HomePage;
