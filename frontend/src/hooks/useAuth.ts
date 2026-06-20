import { useMutation, useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';

interface LoginCredentials {
  email: string;
  password: string;
}

interface SignupCredentials {
  email: string;
  password: string;
}

interface AuthResponse {
  token: string;
  email: string;
  userId: string;
}

interface User {
  email: string;
  userId: string;
  createdAt: string;
  isActive: boolean;
}

export function useAuth() {
  const login = useMutation({
    mutationFn: (credentials: LoginCredentials) =>
      apiClient.post<AuthResponse>('/api/v1/auth/login', credentials),
    onSuccess: (data) => {
      const authData = data.data as AuthResponse;
      localStorage.setItem('token', authData.token);
      localStorage.setItem('userEmail', authData.email);
      localStorage.setItem('userId', authData.userId);
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${authData.token}`;
    },
  });

  const signup = useMutation({
    mutationFn: (credentials: SignupCredentials) =>
      apiClient.post<{ message: string }>('/api/v1/auth/signup', credentials),
  });

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userId');
    delete apiClient.defaults.headers.common['Authorization'];
  };

  const isAuthenticated = () => {
    return !!localStorage.getItem('token');
  };

  const getToken = () => {
    return localStorage.getItem('token');
  };

  const getUserEmail = () => {
    return localStorage.getItem('userEmail');
  };

  return {
    login,
    signup,
    logout,
    isAuthenticated,
    getToken,
    getUserEmail,
  };
}

export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const response = await apiClient.get<User>('/api/v1/auth/me');
      return response.data;
    },
    enabled: !!localStorage.getItem('token'),
    retry: false,
  });
}
