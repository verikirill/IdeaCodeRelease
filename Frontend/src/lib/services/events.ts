// Импортируем константу API_URL
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
 */
export async function getEvent(eventId: number): Promise<Event | null> {
  try {
    const response = await fetch(`${API_URL}/events/${eventId}`);
    
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