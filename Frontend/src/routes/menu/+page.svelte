<script lang="ts">
  import { onMount } from 'svelte';
  import { menuService, type Dish, type DailyMenu } from '$lib/services/menu';
  
  // Store references
  const { dailyMenus, dishes, loading, error, fetchDailyMenus, fetchDishes, fetchDishesForMenu } = menuService;
  
  interface MenuItem {
    id: number;
    title: string;
    image: string;
    description?: string;
    date?: string;
  }
  
  interface Product {
    id: number;
    name: string;
    image: string;
    calories: string;
    nutrients: string;
  }
  
  interface DayMenu {
    day: string;
    dayName: string;
    menuId: number;
    date: string;
    price: number;
    products: Product[];
    selectedProductIndex: number;
    isToday: boolean;
  }
  
  // Get current date info
  const today = new Date();
  const currentDayOfWeek = today.getDay(); // 0 = Sunday, 1 = Monday, etc.
  const currentDateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
  const daysOfWeek = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
  
  // Хиты недели - static for now, can be replaced with API data later
  let weeklyHits: MenuItem[] = [
    {
      id: 1,
      title: 'ПРОТ',
      image: '/menu1.png',
      description: 'ПРОТЕИНОВЫЙ БАТОНЧИК БЕЗ САХАРА СИНКАБАР'
    },
    {
      id: 2,
      title: 'SUSHI',
      image: '/menu2.png',
      description: 'BORA BORA'
    },
    {
      id: 3,
      title: 'БЛИНЫ',
      image: '/menu3.png',
      description: 'SO DELICIOUS!',
      date: '12-18 МАРТА'
    }
  ];
  
  // Дневное меню - will be populated from API
  let daysMenu: DayMenu[] = [];
  let todayMenu: DayMenu | null = null;
  let hasMenuData = false;
  
  // Function to convert API dishes to Product format
  function convertDishToProduct(dish: Dish): Product {
    return {
      id: dish.id,
      name: dish.name,
      // Use dish photo if available, otherwise fallback to static images
      image: dish.photo ? `/static/${dish.photo}` : `/menu1(${Math.floor(Math.random() * 3) + 1}).png`,
      calories: `Калории: ${dish.kilocalories || 0} ккал.`,
      nutrients: `Белки: ${dish.proteins || 0} гр. Жиры: ${dish.fats || 0} гр. Углеводы: ${dish.carbohydrates || 0} гр.`
    };
  }
  
  // Function to convert date to day of week in Russian
  function getDayOfWeek(dateStr: string): string {
    const date = new Date(dateStr);
    return daysOfWeek[date.getDay()];
  }
  
  // Function to format date for display
  function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    const options: Intl.DateTimeFormatOptions = { 
      day: 'numeric', 
      month: 'long',
      year: 'numeric'
    };
    return date.toLocaleDateString('ru-RU', options);
  }
  
  // Function to check if a date is today
  function isToday(dateStr: string): boolean {
    return dateStr.split('T')[0] === currentDateStr;
  }
  
  // Function to format price
  function formatPrice(price: number): string {
    return `${price} ₽`;
  }
  
  // Function to create day menu from API data
  async function createDayMenus() {
    const allDailyMenus = $dailyMenus;
    
    // Check if we have any menus
    if (allDailyMenus.length === 0) {
      hasMenuData = false;
      return;
    }
    
    hasMenuData = true;
    
    // Sort menus by date, putting today's menu first if it exists
    allDailyMenus.sort((a, b) => {
      // Check if either menu is for today
      const aIsToday = isToday(a.date);
      const bIsToday = isToday(b.date);
      
      // If a is today and b is not, a comes first
      if (aIsToday && !bIsToday) return -1;
      // If b is today and a is not, b comes first
      if (!aIsToday && bIsToday) return 1;
      
      // Otherwise sort by date (newest first)
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    });
    
    // Limit to recent menus (include at least today if available)
    const recentMenus = allDailyMenus.slice(0, 7);
    
    // Create day menus from daily menus
    daysMenu = await Promise.all(recentMenus.map(async (menu) => {
      // Get dishes for this menu
      const menuDishes = await fetchDishesForMenu(menu.id);
      const products = menuDishes.map(convertDishToProduct);
      const menuIsToday = isToday(menu.date);
      
      const dayMenu = {
        day: getDayOfWeek(menu.date),
        dayName: formatDate(menu.date),
        menuId: menu.id,
        date: menu.date,
        price: menu.price,
        products: products.length > 0 ? products : [
          // If no dishes are available for this menu
          { 
            id: -1,
            name: 'Нет данных о блюдах', 
            image: '/menu1(1).png',
            calories: 'Нет данных',
            nutrients: 'Нет данных'
          }
        ],
        selectedProductIndex: 0,
        isToday: menuIsToday
      };
      
      // Store today's menu separately if this is it
      if (menuIsToday) {
        todayMenu = dayMenu;
      }
      
      return dayMenu;
    }));
  }
  
  // Функция выбора продукта
  function selectProduct(dayIndex: number, productIndex: number) {
    daysMenu[dayIndex].selectedProductIndex = productIndex;
  }
  
  let currentHitIndex = 0;
  
  function prevHit() {
    if (currentHitIndex > 0) {
      currentHitIndex--;
    } else {
      currentHitIndex = weeklyHits.length - 1;
    }
  }
  
  function nextHit() {
    if (currentHitIndex < weeklyHits.length - 1) {
      currentHitIndex++;
    } else {
      currentHitIndex = 0;
    }
  }
  
  // Function to initialize the menu data
  async function initializeMenuData() {
    // Fetch menus data from API
    await fetchDailyMenus();
    
    // Create day menus from API data
    await createDayMenus();
  }
  
  onMount(() => {
    // Initialize menu data
    initializeMenuData();
    
    // Автоматическое пролистывание карусели каждые 5 секунд
    const interval = setInterval(() => {
      nextHit();
    }, 5000);
    
    return () => {
      clearInterval(interval);
    };
  });
</script>

<div class="container">
  <h1 class="menu-title">Меню столовой</h1>

  {#if $loading}
    <div class="loading">Загрузка меню...</div>
  {:else if $error}
    <div class="error">Ошибка загрузки меню: {$error}</div>
  {:else}
    {#if !hasMenuData}
      <div class="no-data">
        <p>Нет данных о меню. Пожалуйста, проверьте позже.</p>
      </div>
    {:else}
      {#if todayMenu}
        <!-- Today's menu highlight -->
        <div class="today-menu">
          <h2 class="today-title">Сегодняшнее меню <span class="today-icon">🍽️</span></h2>
          <div class="day-card today-card">
            <div class="day-info">
              <div class="calendar-icon today-calendar">
                <span class="day-name">{todayMenu.day}</span>
              </div>
              <div class="meal-info">
                <h3 class="dish-title">{todayMenu.dayName}</h3>
                <p class="price-info">Цена: {formatPrice(todayMenu.price)}</p>
                <p class="calories-info">{todayMenu.products[todayMenu.selectedProductIndex].calories}</p>
                <p class="details">{todayMenu.products[todayMenu.selectedProductIndex].nutrients}</p>
              </div>
            </div>
            
            <div class="products-row">
              {#each todayMenu.products as product, productIndex}
                <div 
                  class="product-item today-product" 
                  class:selected={productIndex === todayMenu.selectedProductIndex}
                  on:click={() => {
                    const dayIndex = daysMenu.findIndex(day => day.isToday);
                    if (dayIndex !== -1) selectProduct(dayIndex, productIndex);
                  }}
                >
                  <div class="product-image-container">
                    <img src={product.image} alt={product.name} class="product-image">
                  </div>
                  <span class="product-name">{product.name}</span>
                </div>
              {/each}
            </div>
          </div>
        </div>
      {:else}
        <div class="no-data">
          <p>Нет данных о меню на сегодняшний день ({formatDate(today.toISOString())}).</p>
        </div>
      {/if}

      <!-- Дневное меню на другие дни -->
      {#if daysMenu.some(day => !day.isToday)}
        <div class="daily-menu">
          <h2 class="section-title">Меню на другие дни</h2>
          {#each daysMenu.filter(day => !day.isToday) as day, dayIndex}
            <div class="day-card">
              <div class="day-info">
                <div class="calendar-icon">
                  <span class="day-name">{day.day}</span>
                </div>
                <div class="meal-info">
                  <h3 class="dish-title">{day.dayName}</h3>
                  <p class="price-info">Цена: {formatPrice(day.price)}</p>
                  <p class="calories-info">{day.products[day.selectedProductIndex].calories}</p>
                  <p class="details">{day.products[day.selectedProductIndex].nutrients}</p>
                </div>
              </div>
              
              <div class="products-row">
                {#each day.products as product, productIndex}
                  <div 
                    class="product-item" 
                    class:selected={productIndex === day.selectedProductIndex}
                    on:click={() => selectProduct(dayIndex, productIndex)}
                  >
                    <div class="product-image-container">
                      <img src={product.image} alt={product.name} class="product-image">
                    </div>
                    <span class="product-name">{product.name}</span>
                  </div>
                {/each}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    {/if}

    <!-- Хиты недели -->
    <div class="hits-section">
      <h2 class="section-title">
        Хиты недели <span class="lightning-icon">⚡</span>
      </h2>
      
      <div class="hits-grid">
        {#each weeklyHits as hit}
          <div class="hit-card">
            <img src={hit.image} alt={hit.title} class="hit-image">
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  /* Контейнер */
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Основные стили для страницы меню */
  .menu-title {
    font-size: 32px;
    margin: 20px 0;
    color: #333;
    text-align: center;
  }
  
  /* Loading and error states */
  .loading, .error, .no-data {
    text-align: center;
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
  }
  
  .loading {
    background-color: #f0f0f0;
  }
  
  .error {
    background-color: #ffebee;
    color: #c62828;
  }
  
  .no-data {
    background-color: #e8f5e9;
    color: #2e7d32;
    font-size: 18px;
  }
  
  /* Today's menu highlight */
  .today-menu {
    margin: 30px 0;
  }
  
  .today-title {
    font-size: 26px;
    margin-bottom: 15px;
    color: #4CAF50;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .today-icon {
    font-size: 24px;
  }
  
  .today-card {
    border: 2px solid #4CAF50;
    background-color: #f8fff8;
  }
  
  .today-calendar {
    background-color: #4CAF50;
  }
  
  .today-product {
    background-color: #f1f8e9;
  }
  
  .product-image-container {
    width: 85px;
    height: 85px;
    overflow: hidden;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  /* Стили для раздела "Хиты недели" */
  .hits-section {
    margin: 30px 0;
  }
  
  .section-title {
    font-size: 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .lightning-icon {
    color: #FFD700;
    font-size: 20px;
  }
  
  /* Стили для грида хитов */
  .hits-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-bottom: 30px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .hit-card {
    aspect-ratio: auto;
    background-color: transparent;
    border-radius: 0;
    overflow: visible;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    max-width: 280px;
    margin: 0 auto;
  }
  
  .hit-image {
    width: 100%;
    height: auto;
    object-fit: contain;
    max-height: 280px;
  }
  
  /* Стили для дневного меню */
  .daily-menu {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 40px;
  }
  
  .day-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f2f2f2;
    border-radius: 15px;
    padding: 15px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .day-info {
    display: flex;
    align-items: center;
    gap: 20px;
  }
  
  .calendar-icon {
    width: 60px;
    height: 60px;
    background-color: #333;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }
  
  .calendar-icon:before {
    display: none;
  }
  
  .calendar-icon:after {
    display: none;
  }
  
  .day-name {
    font-size: 24px;
    font-weight: bold;
    color: white;
  }
  
  .meal-info {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  .dish-title {
    font-size: 24px;
    margin: 0;
    font-weight: bold;
  }
  
  .price-info {
    margin: 0;
    color: #4CAF50;
    font-size: 16px;
    font-weight: bold;
  }
  
  .calories-info {
    margin: 0;
    color: #555;
    font-size: 14px;
  }
  
  .details {
    font-size: 14px;
    color: #666;
    margin: 0;
  }
  
  .products-row {
    display: flex;
    gap: 20px;
    justify-content: flex-end;
    flex-wrap: wrap;
  }
  
  .product-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    width: 110px;
    height: 120px;
    position: relative;
  }
  
  .product-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .product-name {
    font-size: 14px;
    text-align: center;
    position: absolute;
    bottom: 5px;
    max-width: 90%;
    background-color: rgba(255, 255, 255, 0.7);
    padding: 2px 5px;
    border-radius: 4px;
  }
  
  .product-item.selected {
    background-color: #465E44;
  }
  
  .product-item.selected .product-name {
    color: white;
    background-color: rgba(70, 94, 68, 0.8);
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .hits-grid {
      grid-template-columns: 1fr;
    }
    
    .hit-card {
      height: 200px;
    }
    
    .day-card {
      flex-direction: column;
      align-items: flex-start;
      gap: 15px;
    }
    
    .products-row {
      width: 100%;
      justify-content: space-between;
    }
  }
</style>