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

// Вспомогательные функции для работы с cookies
function setCookie(name: string, value: string, days = 7): void {
  if (!browser) return;
  
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
}

function getCookie(name: string): string | null {
  if (!browser) return null;
  
  const nameEQ = name + '=';
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

function deleteCookie(name: string): void {
  if (!browser) return;
  
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;SameSite=Strict`;
}

// Инициализируем хранилища
const createAuthStore = () => {
  // Загружаем начальные значения из cookies (если в браузере)
  const initialToken = browser ? getCookie('access_token') : null;
  const initialUser = browser ? JSON.parse(getCookie('user_data') || 'null') : null;
  
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
        setCookie('access_token', data.access_token);
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
        // Если получили 401 Unauthorized, очищаем токен и данные пользователя
        if (response.status === 401) {
          token.set(null);
          user.set(null);
          
          if (browser) {
            deleteCookie('access_token');
            deleteCookie('user_data');
          }
          
          // Но НЕ делаем автоматическое перенаправление на страницу логина
          return null;
        }
        
        throw new Error('Не удалось получить данные пользователя');
      }
      
      const userData: UserData = await response.json();
      user.set(userData);
      
      if (browser) {
        setCookie('user_data', JSON.stringify(userData));
      }
      
      return userData;
    } catch (error) {
      console.error('Error fetching user data:', error);
      // Если запрос не удался, попробуем использовать кэшированные данные
      if (browser) {
        const cachedUser = getCookie('user_data');
        if (cachedUser) {
          const userData = JSON.parse(cachedUser);
          user.set(userData);
          return userData;
        }
      }
      return null;
    }
  }
  
  // Функция для обновления профиля пользователя
  async function updateUserProfile(userData: Partial<UserData>): Promise<boolean> {
    try {
      let currentToken: string | null = null;
      token.subscribe(value => {
        currentToken = value;
      })();
      
      if (!currentToken) {
        return false;
      }
      
      // Отправляем запрос на обновление профиля
      const response = await fetch(`${API_URL}/users/update-profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${currentToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });
      
      if (!response.ok) {
        throw new Error('Не удалось обновить данные пользователя');
      }
      
      // Получаем обновленные данные
      const updatedUser = await response.json();
      user.set(updatedUser);
      
      if (browser) {
        setCookie('user_data', JSON.stringify(updatedUser));
      }
      
      return true;
    } catch (error) {
      console.error('Error updating user profile:', error);
      return false;
    }
  }
  
  // Функция для загрузки аватара
  async function uploadAvatar(file: File): Promise<boolean> {
    try {
      let currentToken: string | null = null;
      token.subscribe(value => {
        currentToken = value;
      })();
      
      if (!currentToken) {
        return false;
      }
      
      // Создаем FormData для отправки файла
      const formData = new FormData();
      formData.append('file', file);
      
      // Отправляем запрос на загрузку аватара
      const response = await fetch(`${API_URL}/users/upload-avatar`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${currentToken}`
        },
        body: formData
      });
      
      if (!response.ok) {
        throw new Error('Не удалось загрузить аватар');
      }
      
      // Получаем обновленные данные пользователя
      const updatedUser = await response.json();
      user.set(updatedUser);
      
      if (browser) {
        setCookie('user_data', JSON.stringify(updatedUser));
      }
      
      return true;
    } catch (error) {
      console.error('Error uploading avatar:', error);
      return false;
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
        setCookie('user_data', JSON.stringify(userData));
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
      deleteCookie('access_token');
      deleteCookie('user_data');
      
      // Получаем текущий путь
      const currentPath = window.location.pathname;
      // Перенаправляем на страницу логина только если мы не на странице логина или регистрации
      if (currentPath !== '/login' && currentPath !== '/register') {
        goto('/login');
      }
    }
  }
  
  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUserData,
    updateUserProfile,
    uploadAvatar
  };
};

// Экспортируем синглтон
export const authStore = createAuthStore(); 