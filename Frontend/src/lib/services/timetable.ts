// Импортируем зависимости
import { authStore } from './auth';
import { browser } from '$app/environment';

// Базовый URL API
const API_URL = browser 
  ? (window.location.hostname === 'localhost' ? 'http://localhost:8000' : window.location.origin)
  : 'http://localhost:8000'; // Значение по умолчанию для серверного рендеринга

export interface Group {
  id: number;
  number: string;
  name?: string;
}

export interface Lesson {
  id: number;
  subject: {
    id: number;
    name: string;
  };
  weekday: number;
  number: number;
  start_time: string;
  end_time: string;
  odd_week: boolean;
  even_week: boolean;
  teachers: {
    id: number;
    name: string;
  }[];
  places: {
    id: number;
    name: string;
  }[];
}

// Функция для поиска групп
export async function searchGroups(query: string): Promise<Group[]> {
  try {
    if (!query) return [];
    
    const response = await fetch(`${API_URL}/timetable/search_group?query=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      throw new Error(`Ошибка при поиске групп: ${response.statusText}`);
    }
    
    const groups = await response.json();
    return groups;
  } catch (error) {
    console.error('Ошибка при поиске групп:', error);
    return [];
  }
}

// Функция для получения выбранной группы пользователя
export async function getUserGroup(): Promise<Group | null> {
  try {
    const token = getToken();
    if (!token) return null;
    
    const response = await fetch(`${API_URL}/timetable/user/group`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        return null; // Группа не выбрана
      }
      throw new Error(`Ошибка при получении группы: ${response.statusText}`);
    }
    
    const data = await response.json();
    // Маппим поля из ответа API в формат Group
    return {
      id: data.group_id,
      number: data.group_number,
      name: data.group_name
    };
  } catch (error) {
    console.error('Ошибка при получении выбранной группы:', error);
    return null;
  }
}

// Функция для выбора группы пользователя
export async function selectUserGroup(groupId: number): Promise<boolean> {
  try {
    const token = getToken();
    if (!token) return false;
    
    const response = await fetch(`${API_URL}/timetable/user/select-group`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ group_id: groupId })
    });
    
    if (!response.ok) {
      throw new Error(`Ошибка при выборе группы: ${response.statusText}`);
    }
    
    return true;
  } catch (error) {
    console.error('Ошибка при выборе группы:', error);
    return false;
  }
}

// Функция для получения расписания пользователя
export async function getUserSchedule(): Promise<Lesson[]> {
  try {
    const token = getToken();
    if (!token) return [];
    
    const response = await fetch(`${API_URL}/timetable/user/schedule`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Ошибка при получении расписания: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Преобразуем формат данных, если нужно
    const lessons: Lesson[] = data.map((item: any) => {
      // Проверка данных о местах проведения
      const places = [];
      if (item.places) {
        if (Array.isArray(item.places)) {
          for (const place of item.places) {
            if (typeof place === 'object' && place.name) {
              places.push(place);
            } else if (typeof place === 'string') {
              places.push({ id: 0, name: place });
            }
          }
        } else if (typeof item.places === 'string') {
          // Если места переданы как строка
          places.push({ id: 0, name: item.places });
        }
      }
      
      return {
        id: item.id,
        subject: {
          id: typeof item.subject === 'object' ? item.subject.id : 0,
          name: typeof item.subject === 'object' ? item.subject.name : item.subject
        },
        weekday: item.weekday,
        number: item.number,
        start_time: item.start_time,
        end_time: item.end_time,
        odd_week: item.odd_week,
        even_week: item.even_week,
        teachers: Array.isArray(item.teachers) ? item.teachers : [],
        places: places
      };
    });
    
    return lessons;
  } catch (error) {
    console.error('Ошибка при получении расписания:', error);
    return [];
  }
}

// Функция для получения расписания пользователя на сегодня
export async function getUserScheduleToday(): Promise<Lesson[]> {
  try {
    const token = getToken();
    if (!token) return [];
    
    const response = await fetch(`${API_URL}/timetable/user/schedule/today`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Ошибка при получении расписания: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Ошибка при получении расписания на сегодня:', error);
    return [];
  }
}

// Функция для получения расписания пользователя по дню недели
export async function getUserScheduleByDay(weekday: number, weekType?: string): Promise<Lesson[]> {
  try {
    const token = getToken();
    if (!token) return [];
    
    let url = `${API_URL}/timetable/user/schedule/day/${weekday}`;
    if (weekType) {
      url += `?week_type=${weekType}`;
    }
    
    console.log(`Запрос расписания по дню: ${url}`);
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Ошибка при получении расписания: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log(`Получено расписание для дня ${weekday}, тип недели: ${weekType}`, data);
    
    // Преобразуем формат данных, если нужно
    const lessons: Lesson[] = data.map((item: any) => {
      // Проверка данных о местах проведения
      const places = [];
      if (item.places) {
        if (Array.isArray(item.places)) {
          for (const place of item.places) {
            if (typeof place === 'object' && place.name) {
              places.push(place);
            } else if (typeof place === 'string') {
              places.push({ id: 0, name: place });
            }
          }
        } else if (typeof item.places === 'string') {
          // Если места переданы как строка
          places.push({ id: 0, name: item.places });
        }
      }
      
      console.log(`Места проведения для предмета "${item.subject}":`, places);
      
      return {
        id: item.id,
        subject: {
          id: typeof item.subject === 'object' ? item.subject.id : 0,
          name: typeof item.subject === 'object' ? item.subject.name : item.subject
        },
        weekday: item.weekday,
        number: item.number,
        start_time: item.start_time,
        end_time: item.end_time,
        odd_week: item.odd_week,
        even_week: item.even_week,
        teachers: Array.isArray(item.teachers) ? item.teachers : [],
        places: places
      };
    });
    
    return lessons;
  } catch (error) {
    console.error(`Ошибка при получении расписания на день ${weekday}:`, error);
    return [];
  }
}

// Функция для получения расписания конкретной группы
export async function getGroupSchedule(groupId: number): Promise<Lesson[]> {
  try {
    const response = await fetch(`${API_URL}/timetable/group/${groupId}/schedule`);
    
    if (!response.ok) {
      throw new Error(`Ошибка при получении расписания группы: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Ошибка при получении расписания группы ${groupId}:`, error);
    return [];
  }
}

// Вспомогательная функция для получения токена
function getToken(): string {
  let token = '';
  authStore.token.subscribe(value => {
    token = value || '';
  })();
  return token;
} 