// Импортируем константу API_URL и authStore для получения токена
import { authStore } from './auth';
const API_URL = 'http://localhost:8000'; // Базовый URL API

export interface Event {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  location: string;
  max_participants: number;
  price: number;
  is_team_event: boolean;
  created_at: string;
  participants: number[];
  image_url?: string;
}

export interface EventDetail {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  location: string;
  max_participants: number;
  current_participants: number;
  price: number;
  is_team_event: boolean;
  created_at: string;
  is_registered: boolean;
}

export interface RegistrationResponse {
  success: boolean;
  message: string;
  event_id: number;
  user_id: number;
}

export interface EventParticipant {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  avatar: string;
}

/**
 * Получение списка всех событий
 */
export async function getEvents(): Promise<Event[]> {
  try {
    const response = await fetch(`${API_URL}/events`);
    
    if (!response.ok) {
      throw new Error(`Error fetching events: ${response.statusText}`);
    }
    
    const events = await response.json();
    return events;
  } catch (error) {
    console.error('Failed to fetch events:', error);
    return [];
  }
}

/**
 * Получение изображений галереи для события
 */
export async function getEventImages(eventId: number): Promise<string[]> {
  try {
    const response = await fetch(`${API_URL}/gallery?event_id=${eventId}`);
    
    if (!response.ok) {
      throw new Error(`Error fetching gallery images: ${response.statusText}`);
    }
    
    const images = await response.json();
    return images.map((image: any) => image.image_url);
  } catch (error) {
    console.error(`Failed to fetch images for event ${eventId}:`, error);
    return [];
  }
}

/**
 * Получение детальной информации о событии
 * Включает информацию о том, зарегистрирован ли текущий пользователь
 */
export async function getEventDetail(eventId: number): Promise<EventDetail | null> {
  try {
    let accessToken = '';
    authStore.token.subscribe((token) => {
      accessToken = token || '';
    })();
    
    if (!accessToken) {
      throw new Error('Для просмотра деталей событий необходимо авторизоваться');
    }
    
    const response = await fetch(`${API_URL}/events/${eventId}`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error fetching event: ${response.statusText}`);
    }
    
    const event = await response.json();
    return event;
  } catch (error) {
    console.error(`Failed to fetch event ${eventId}:`, error);
    return null;
  }
}

/**
 * Регистрация на событие
 */
export async function registerForEvent(eventId: number): Promise<RegistrationResponse> {
  try {
    let accessToken = '';
    authStore.token.subscribe((token) => {
      accessToken = token || '';
    })();
    
    if (!accessToken) {
      throw new Error('Для регистрации на событие необходимо авторизоваться');
    }
    
    const response = await fetch(`${API_URL}/events/${eventId}/register`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при регистрации на событие');
    }
    
    const result = await response.json();
    return result;
  } catch (error: any) {
    console.error(`Failed to register for event ${eventId}:`, error);
    return {
      success: false,
      message: error.message || 'Произошла ошибка при регистрации на событие',
      event_id: eventId,
      user_id: 0
    };
  }
}

/**
 * Отмена регистрации на событие
 */
export async function unregisterFromEvent(eventId: number): Promise<RegistrationResponse> {
  try {
    let accessToken = '';
    authStore.token.subscribe((token) => {
      accessToken = token || '';
    })();
    
    if (!accessToken) {
      throw new Error('Для отмены регистрации на событие необходимо авторизоваться');
    }
    
    const response = await fetch(`${API_URL}/events/${eventId}/register`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при отмене регистрации на событие');
    }
    
    const result = await response.json();
    return result;
  } catch (error: any) {
    console.error(`Failed to unregister from event ${eventId}:`, error);
    return {
      success: false,
      message: error.message || 'Произошла ошибка при отмене регистрации на событие',
      event_id: eventId,
      user_id: 0
    };
  }
}

/**
 * Получение списка участников события
 */
export async function getEventParticipants(eventId: number): Promise<EventParticipant[]> {
  try {
    let accessToken = '';
    authStore.token.subscribe((token) => {
      accessToken = token || '';
    })();
    
    if (!accessToken) {
      throw new Error('Для просмотра участников необходимо авторизоваться');
    }
    
    const response = await fetch(`${API_URL}/events/${eventId}/participants`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error fetching participants: ${response.statusText}`);
    }
    
    const participants = await response.json();
    return participants;
  } catch (error) {
    console.error(`Failed to fetch participants for event ${eventId}:`, error);
    return [];
  }
} 