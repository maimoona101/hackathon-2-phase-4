'use client';

import './globals.css';
import { AuthProvider, useAuth } from '../lib/auth'; // ✅ useAuth add kiya

function Navbar() {
  const { logout, isAuthenticated } = useAuth(); // ✅ auth hook

  return (
    <nav className="flex items-center space-x-4">
      <a
        href="/"
        className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
      >
        Home
      </a>

      {isAuthenticated && (
        <button
          onClick={() => {
            logout();
            window.location.href = '/login';
          }}
          className="bg-red-500 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-red-600"
        >
          Logout
        </button>
      )}
    </nav>
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50">
            <header className="bg-white shadow">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                  <div className="flex">
                    <div className="flex-shrink-0 flex items-center">
                      <span className="text-xl font-bold text-gray-900">Todo App</span>
                    </div>
                  </div>
                  <Navbar /> {/* ✅ Navbar component use */}
                </div>
              </div>
            </header>
            <main>{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
