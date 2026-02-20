'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { apiClient } from './api';

interface User {
  id: string;
  email: string;
  display_name?: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, displayName?: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem('auth_token'); // ✅ read token
    if (savedToken) {
      setToken(savedToken);
      apiClient.setAuthToken(savedToken); // optional: set header
      apiClient
        .request('/api/users/profile')
        .then((userData) => {
          setUser(userData);
        })
        .catch(() => {
          localStorage.removeItem('auth_token');
          setToken(null);
          setUser(null);
        });
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const data = await apiClient.login(email, password);
    setToken(data.access_token);
    localStorage.setItem('auth_token', data.access_token); // ✅ persist token

    const userData = await apiClient.request('/api/users/profile');
    setUser(userData);
  };

  const register = async (email: string, password: string, displayName?: string) => {
    await apiClient.register(email, password, displayName);
    await login(email, password);
  };

  const logout = () => {
    apiClient.logout();
    setToken(null);
    setUser(null);
    localStorage.removeItem('auth_token'); // ✅ remove token
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!token,
  };

  if (loading) return null;

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
