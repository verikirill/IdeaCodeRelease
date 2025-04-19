import { writable } from 'svelte/store';
import { authStore } from './auth';

// Types
export interface Dish {
  id: number;
  name: string;
  description?: string;
  composition?: string;
  proteins?: number;
  fats?: number;
  carbohydrates?: number;
  kilocalories?: number;
  price: number;
  photo?: string;
  category_id: number;
  is_available?: boolean;
  created_at: string;
  updated_at?: string;
}

export interface DailyMenu {
  id: number;
  date: string;
  price: number;
  dishes: number[];
  created_at: string;
  updated_at?: string;
}

// API URL
const API_URL = 'http://localhost:8000';

// Create stores
const dailyMenus = writable<DailyMenu[]>([]);
const dishes = writable<Dish[]>([]);
const loading = writable<boolean>(false);
const error = writable<string | null>(null);

// Function to fetch all daily menus
async function fetchDailyMenus(): Promise<DailyMenu[]> {
  loading.set(true);
  error.set(null);
  
  try {
    const response = await fetch(`${API_URL}/menu`);
    
    if (!response.ok) {
      throw new Error(`Error fetching daily menus: ${response.statusText}`);
    }
    
    const data: DailyMenu[] = await response.json();
    dailyMenus.set(data);
    return data;
  } catch (err) {
    console.error('Failed to fetch daily menus:', err);
    error.set(err instanceof Error ? err.message : 'Unknown error occurred');
    return [];
  } finally {
    loading.set(false);
  }
}

// Function to fetch a single daily menu
async function fetchDailyMenu(id: number): Promise<DailyMenu | null> {
  loading.set(true);
  error.set(null);
  
  try {
    const response = await fetch(`${API_URL}/menu/${id}`);
    
    if (!response.ok) {
      throw new Error(`Error fetching daily menu: ${response.statusText}`);
    }
    
    const data: DailyMenu = await response.json();
    return data;
  } catch (err) {
    console.error(`Failed to fetch daily menu ${id}:`, err);
    error.set(err instanceof Error ? err.message : 'Unknown error occurred');
    return null;
  } finally {
    loading.set(false);
  }
}

// Function to fetch all dishes
async function fetchDishes(): Promise<Dish[]> {
  loading.set(true);
  error.set(null);
  
  try {
    // The endpoint is /dish according to the dish_router
    const response = await fetch(`${API_URL}/dish`);
    
    if (!response.ok) {
      throw new Error(`Error fetching dishes: ${response.statusText}`);
    }
    
    const data: Dish[] = await response.json();
    dishes.set(data);
    return data;
  } catch (err) {
    console.error('Failed to fetch dishes:', err);
    error.set(err instanceof Error ? err.message : 'Unknown error occurred');
    return [];
  } finally {
    loading.set(false);
  }
}

// Function to fetch a single dish
async function fetchDish(id: number): Promise<Dish | null> {
  try {
    const response = await fetch(`${API_URL}/dish/${id}`);
    
    if (!response.ok) {
      throw new Error(`Error fetching dish: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (err) {
    console.error(`Failed to fetch dish ${id}:`, err);
    return null;
  }
}

// Function to fetch all dishes for a specific daily menu
async function fetchDishesForMenu(menuId: number): Promise<Dish[]> {
  const menu = await fetchDailyMenu(menuId);
  if (!menu) return [];
  
  // Fetch dishes in parallel for better performance
  const dishPromises = menu.dishes.map(dishId => fetchDish(dishId));
  const results = await Promise.all(dishPromises);
  
  // Filter out any null results (failed fetches)
  return results.filter((dish): dish is Dish => dish !== null);
}

// Expose the service
export const menuService = {
  dailyMenus,
  dishes,
  loading,
  error,
  fetchDailyMenus,
  fetchDailyMenu,
  fetchDishes,
  fetchDish,
  fetchDishesForMenu
}; 