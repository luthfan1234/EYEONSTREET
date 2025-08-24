// context/AuthContext.tsx

'use client';

import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import axios from '@/lib/axios';
import { mockLogin } from '@/lib/mock-auth';

interface User {
  id: number;
  name: string;
  email: string;
  email_verified_at: string | null;
}

interface AuthContextType {
  user: User | null;
  login: (credentials: { email: string, password: string }) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fungsi untuk mengambil data user saat aplikasi dimuat
  const fetchUser = async () => {
    try {
      const response = await axios.get('/api/user');
      setUser(response.data);
    } catch (error) {
      console.log('User not authenticated:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Skip initial fetch if we're on the landing page
    if (typeof window !== 'undefined' && window.location.pathname === '/landing') {
      setIsLoading(false);
      return;
    }
    fetchUser();
  }, []);

  const login = async (credentials: { email: string, password: string }) => {
    try {
      // Try Laravel backend first
      await axios.get('/sanctum/csrf-cookie');
      await axios.post('/login', credentials);
      await fetchUser();
    } catch (error) {
      console.error('Laravel backend error, using mock auth:', error);
      
      // Fallback to mock auth for development
      try {
        const mockUserData = await mockLogin(credentials);
        setUser(mockUserData);
      } catch (mockError) {
        throw mockError;
      }
    }
  };

  const logout = async () => {
    try {
      // Try Laravel backend logout
      await axios.post('/logout');
    } catch (error) {
      console.log('Laravel backend logout failed, using mock logout:', error);
      // If backend logout fails (like 401), still proceed to clear user state
    } finally {
      // Always clear user state regardless of backend response
      setUser(null);
      
      // Clear any stored tokens/session data
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        sessionStorage.removeItem('auth_token');
      }
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth harus digunakan di dalam AuthProvider');
  }
  return context;
};
