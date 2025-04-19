import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';

// Типы данных
export interface UserData {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: string;
  avatar: string;
  is_active: boolean;
  is_admin: boolean;
  bio?: string;
  phone?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  password: string;
  role?: string;
  gender?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// API URL
const API_URL = 'http://localhost:8000'; // Базовый URL API

// Инициализируем хранилища
const createAuthStore = () => {
  // Загружаем начальные значения из localStorage (если в браузере)
  const initialToken = browser ? localStorage.getItem('access_token') : null;
  const initialUser = browser ? JSON.parse(localStorage.getItem('user') || 'null') : null;
  
  // Создаем Svelte хранилища
  const token = writable<string | null>(initialToken);
  const user = writable<UserData | null>(initialUser);
  const isAuthenticated = derived(token, $token => !!$token);
  
  // Функция для входа
  async function login(credentials: LoginCredentials): Promise<boolean> {
    try {
      // Формируем данные для отправки в формате x-www-form-urlencoded
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);
      
      const response = await fetch(`${API_URL}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка авторизации');
      }
      
      const data: AuthResponse = await response.json();
      
      // Сохраняем токен
      token.set(data.access_token);
      
      if (browser) {
        localStorage.setItem('access_token', data.access_token);
      }
      
      // Получаем данные пользователя после успешного логина
      await fetchUserData();
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }
  
  // Функция для получения данных пользователя
  async function fetchUserData(): Promise<UserData | null> {
    try {
      let currentToken: string | null = null;
      token.subscribe(value => {
        currentToken = value;
      })();
      
      if (!currentToken) {
        return null;
      }
      
      // Делаем запрос на сервер для получения данных пользователя
      const response = await fetch(`${API_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${currentToken}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Не удалось получить данные пользователя');
      }
      
      const userData: UserData = await response.json();
      user.set(userData);
      
      if (browser) {
        localStorage.setItem('user', JSON.stringify(userData));
      }
      
      return userData;
    } catch (error) {
      console.error('Error fetching user data:', error);
      // Если запрос не удался, попробуем использовать кэшированные данные
      if (browser) {
        const cachedUser = localStorage.getItem('user');
        if (cachedUser) {
          const userData = JSON.parse(cachedUser);
          user.set(userData);
          return userData;
        }
      }
      return null;
    }
  }
  
  // Функция для регистрации
  async function register(data: RegisterData): Promise<boolean> {
    try {
      const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка регистрации');
      }
      
      const userData = await response.json();
      if (browser) {
        localStorage.setItem('user', JSON.stringify(userData));
      }
      
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  }
  
  // Функция для выхода
  function logout() {
    token.set(null);
    user.set(null);
    
    if (browser) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
    
    goto('/login');
  }
  
  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUserData
  };
};

// Экспортируем синглтон
export const authStore = createAuthStore(); 