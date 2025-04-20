<script lang="ts">
  import { onMount } from 'svelte';
  import { menuService, type Dish, type DailyMenu, getPhotoUrl } from '$lib/services/menu';
  
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
      // Use getPhotoUrl helper to generate correct URL
      image: dish.photo ? getPhotoUrl(dish.photo) : `/menu1(${Math.floor(Math.random() * 3) + 1}).png`,
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
  
  // Функция выбора продукта с обновлением UI
  function selectProduct(dayIndex: number, productIndex: number) {
    // Обновляем выбранный индекс
    daysMenu[dayIndex].selectedProductIndex = productIndex;
    
    // Если это сегодняшний день, обновляем и todayMenu
    if (daysMenu[dayIndex].isToday && todayMenu) {
      todayMenu.selectedProductIndex = productIndex;
    }
    
    // Форсируем обновление переменных для реактивности
    daysMenu = [...daysMenu];
    if (todayMenu) {
      todayMenu = {...todayMenu};
    }
  }
  
  let currentHitIndex = 0; // Оставим на случай, если потребуется в будущем
  let tickerSpeed = 30; // секунд для полного прохода

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
    
    // Устанавливаем начальную продолжительность анимации
    const ticker = document.querySelector('.ticker');
    if (ticker) {
      ticker.style.animationDuration = `${tickerSpeed}s`;
    }
    
    return () => {
      // Ничего не нужно очищать
    };
  });
</script>

<div class="container">
  <div class="header-section">
    <h1 class="menu-title">Меню столовой</h1>
    <div class="header-line"></div>
  </div>

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
          <h2 class="today-title">Сегодняшнее меню</h2>
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
          {#each daysMenu.filter(day => !day.isToday) as day, filteredDayIndex}
            {@const dayIndex = daysMenu.findIndex(d => d.menuId === day.menuId)}
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
      
      <div class="ticker-container">
        <div class="ticker">
          {#each [...weeklyHits, ...weeklyHits] as hit, i}
            <div class="ticker-item">
              <div class="hit-card">
                <img src={hit.image} alt={hit.title} class="hit-image">
              </div>
            </div>
          {/each}
        </div>
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

  /* Секция заголовка */
  .header-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 40px 0 50px;
    position: relative;
    padding-bottom: 10px;
  }

  .header-section:before {
    content: "";
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 4px;
    background-color: #333;
    border-radius: 2px;
    opacity: 0.2;
  }

  /* Основные стили для заголовка страницы меню */
  .menu-title {
    font-size: 38px;
    color: #222;
    text-align: center;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin: 0;
    position: relative;
  }

  .header-line {
    height: 3px;
    width: 150px;
    background: linear-gradient(to right, rgba(51,51,51,0.1), rgba(51,51,51,0.8), rgba(51,51,51,0.1));
    margin-top: 15px;
    border-radius: 2px;
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
    margin: 40px 0 30px;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
  }
  
  .today-title {
    font-size: 28px;
    margin-bottom: 20px;
    color: #000000;
    font-weight: 600;
    text-align: left;
    letter-spacing: 0.5px;
    position: relative;
    padding-left: 0;
    margin-left: 0;
  }
  
  .today-card {
    border: 2px solid #e0e0e0;
    background-color: #ffffff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    width: 100%;
    max-width: 1100px;
    border-radius: 15px;
    margin-top: 5px;
  }
  
  .today-calendar {
    background-color: #333;
  }
  
  .today-product {
    background-color: #f5f5f5;
  }
  
  .product-image-container {
    width: 85px;
    height: 85px;
    overflow: hidden;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f9f9f9;
    border: 1px solid #eee;
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
  
  /* Стили для бегущей строки "Хиты недели" */
  .ticker-container {
    width: 100%;
    overflow: hidden;
    position: relative;
    padding: 20px 0;
    margin-bottom: 30px;
    background-color: #f8f8f8;
    border-radius: 15px;
    box-shadow: inset 0 0 15px rgba(0,0,0,0.05);
  }
  
  .ticker-container:before,
  .ticker-container:after {
    content: "";
    position: absolute;
    top: 0;
    width: 150px;
    height: 100%;
    z-index: 2;
    pointer-events: none;
  }
  
  .ticker-container:before {
    left: 0;
    background: linear-gradient(to right, #f8f8f8, rgba(248, 248, 248, 0));
  }
  
  .ticker-container:after {
    right: 0;
    background: linear-gradient(to left, #f8f8f8, rgba(248, 248, 248, 0));
  }
  
  .ticker {
    display: flex;
    animation: ticker-scroll 30s linear infinite;
    width: max-content;
    padding: 10px 0;
  }
  
  .ticker-item {
    padding: 0 25px;
    flex-shrink: 0;
  }
  
  .hit-card {
    width: 320px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 2px solid transparent;
    overflow: hidden;
    position: relative;
  }
  
  .hit-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    border-color: rgba(76, 175, 80, 0.3);
  }
  
  .hit-image {
    width: 100%;
    height: 240px;
    object-fit: cover;
    border-radius: 8px;
  }
  
  @keyframes ticker-scroll {
    0% {
      transform: translateX(0);
    }
    100% {
      transform: translateX(-50%);
    }
  }
  
  /* Приостанавливаем анимацию при наведении */
  .ticker-container:hover .ticker {
    animation-play-state: paused;
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
    padding: 10px 15px;
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
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
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
    gap: 6px;
  }
  
  .dish-title {
    font-size: 24px;
    margin: 0;
    font-weight: bold;
    color: #333;
  }
  
  .price-info {
    margin: 0;
    color: #333;
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
    justify-content: flex-start;
    flex-wrap: nowrap;
    overflow-x: auto;
    scroll-behavior: smooth;
    padding: 10px 0;
    margin: 0 -10px;
    scrollbar-width: thin;
    padding-bottom: 20px;
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
    transition: all 0.3s ease;
    width: 110px;
    height: 120px;
    position: relative;
    margin: 0 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border: 2px solid transparent;
  }
  
  .product-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border-color: #4CAF50;
  }
  
  .product-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
  
  .product-item:hover .product-image {
    transform: scale(1.1);
  }
  
  .product-item.selected {
    background-color: #2F4F2F; /* Темно-зеленый цвет */
    border-color: #2F4F2F;
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(47,79,47,0.3);
  }
  
  .product-item.selected .product-name {
    color: white;
    background-color: rgba(47, 79, 47, 0.8); /* Темно-зеленый с прозрачностью */
  }
  
  .product-item.selected .product-image {
    transform: scale(1.05);
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
    transition: all 0.3s ease;
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .hit-card {
      width: 280px;
      height: auto;
    }
    
    .hit-image {
      height: 200px;
    }
    
    .ticker-item {
      padding: 0 15px;
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

  @media (max-width: 480px) {
    .ticker-container {
      padding: 15px 0;
    }
    
    .hit-card {
      width: 240px;
    }
    
    .hit-image {
      height: 180px;
    }
  }

  /* Скрываем стандартный скроллбар в Chrome */
  .products-row::-webkit-scrollbar {
    height: 4px;
  }

  .products-row::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  .products-row::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
  }

  .products-row::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

  /* Адаптивность для заголовка */
  @media (max-width: 768px) {
    .header-section {
      margin: 30px 0 40px;
    }
    
    .menu-title {
      font-size: 32px;
    }
    
    .header-line {
      width: 120px;
    }
  }
</style>