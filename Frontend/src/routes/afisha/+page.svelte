<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/services/auth';
  import { registerForEvent, unregisterFromEvent } from '$lib/services/events';
  import { goto } from '$app/navigation';

  let avatar = '/avatar.png';
  let loading = true;
  let error = null;
  let isAuthenticated = false;
  let selectedEventId = 0;
  let isRegistering = false;
  
  interface Event {
    id: number;
    title: string;
    description: string;
    image: string;
    tag: string;
    fullDescription: string;
    start_date?: string;
    end_date?: string;
    created_at?: string;
    is_registered?: boolean;
    current_participants?: number;
    max_participants?: number;
  }

  // Тестовые данные как запасной вариант
  let events: Event[] = [];
  
  // Состояние сортировки
  let sortOrder = "default"; // default, newest, oldest
  
  // URL нашего API
  const API_URL = 'http://localhost:8000';
  
  // Функция для форматирования даты
  function formatDate(dateString: string): string {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    
    // Получаем день и месяц
    const day = date.getDate().toString().padStart(2, '0');
    
    // Массив с названиями месяцев
    const months = [
      'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
      'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ];
    const month = months[date.getMonth()];
    
    return `${day} ${month}`;
  }
  
  // Функция для сравнения дат (только день и месяц)
  function areSameDates(date1: string, date2: string): boolean {
    if (!date1 || !date2) return false;
    
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    
    return d1.getDate() === d2.getDate() && d1.getMonth() === d2.getMonth();
  }
  
  // Функция для загрузки данных
  async function loadEvents() {
    try {
      loading = true;
      error = null;
      
      // Получаем статус аутентификации
      const unsubscribe = authStore.isAuthenticated.subscribe(value => {
        isAuthenticated = value;
      });
      unsubscribe();
      
      // URL для загрузки данных
      let url = `${API_URL}/events/afisha`;
      
      const response = await fetch(url, {
        headers: isAuthenticated ? {
          'Authorization': `Bearer ${getToken()}`
        } : {}
      });
      
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      events = data;
      
      // Если пользователь авторизован, получаем дополнительную информацию о событиях
      if (isAuthenticated) {
        await Promise.all(events.map(async (event) => {
          try {
            const detailResponse = await fetch(`${API_URL}/events/${event.id}`, {
              headers: {
                'Authorization': `Bearer ${getToken()}`
              }
            });
            
            if (detailResponse.ok) {
              const detailData = await detailResponse.json();
              event.is_registered = detailData.is_registered;
              event.current_participants = detailData.current_participants;
              event.max_participants = detailData.max_participants;
            }
          } catch (e) {
            console.error(`Не удалось получить детали для события ${event.id}:`, e);
          }
        }));
      }
      
    } catch (err) {
      console.error('Ошибка при загрузке событий:', err);
      error = err.message;
      // Используем тестовые данные в случае ошибки
      events = [
        {
          id: 1,
          title: 'Универсиада «Ломоносов» 2025',
          description: 'МГУ приглашает студентов принять участие в Универсиаде "Ломоносов" по математическим методам в экономике. Отличная возможность для развития математических навыков.',
          image: '/event1.png',
          tag: '#Универсиада',
          fullDescription: 'Полное описание Универсиады «Ломоносов» 2025',
          start_date: '2025-03-15T10:00:00',
          end_date: '2025-03-20T18:00:00',
          created_at: '2023-05-15T10:00:00',
          is_registered: false,
          current_participants: 42,
          max_participants: 100
        },
        {
          id: 2,
          title: 'Путёвки в здравницы МГУ',
          description: 'С 20.02.2025 реализуются путёвки в здравницы МГУ на сезон 2025 года. Оформление путёвок в отделе реализации социальных программ.',
          image: '/event2.png',
          tag: '#Университетская жизнь',
          fullDescription: 'Полное описание путёвок в здравницы МГУ',
          start_date: '2025-02-20T09:00:00',
          end_date: '2025-04-30T18:00:00',
          created_at: '2023-06-20T10:00:00',
          is_registered: false,
          current_participants: 15,
          max_participants: 50
        }
      ];
    } finally {
      loading = false;
      sortEvents();
    }
  }
  
  // Получение токена авторизации
  function getToken(): string {
    let token = '';
    authStore.token.subscribe(value => {
      token = value || '';
    })();
    return token;
  }
  
  // Регистрация на событие
  async function handleRegister(eventId: number) {
    try {
      if (!isAuthenticated) {
        goto('/login?redirect=/afisha');
        return;
      }
      
      isRegistering = true;
      selectedEventId = eventId;
      
      const result = await registerForEvent(eventId);
      
      if (result.success) {
        // Обновляем статус регистрации в списке событий
        const eventIndex = events.findIndex(e => e.id === eventId);
        if (eventIndex !== -1) {
          events[eventIndex].is_registered = true;
          if (events[eventIndex].current_participants !== undefined) {
            events[eventIndex].current_participants += 1;
          }
          events = [...events]; // Для обновления UI
        }
      }
    } catch (err: any) {
      console.error('Ошибка при регистрации:', err);
    } finally {
      isRegistering = false;
    }
  }
  
  // Отмена регистрации на событие
  async function handleUnregister(eventId: number) {
    try {
      if (!isAuthenticated) {
        goto('/login?redirect=/afisha');
        return;
      }
      
      isRegistering = true;
      selectedEventId = eventId;
      
      const result = await unregisterFromEvent(eventId);
      
      if (result.success) {
        // Обновляем статус регистрации в списке событий
        const eventIndex = events.findIndex(e => e.id === eventId);
        if (eventIndex !== -1) {
          events[eventIndex].is_registered = false;
          if (events[eventIndex].current_participants !== undefined && events[eventIndex].current_participants > 0) {
            events[eventIndex].current_participants -= 1;
          }
          events = [...events]; // Для обновления UI
        }
      }
    } catch (err: any) {
      console.error('Ошибка при отмене регистрации:', err);
    } finally {
      isRegistering = false;
    }
  }
  
  // Функция для сортировки событий
  function sortEvents() {
    if (sortOrder === "newest") {
      events = [...events].sort((a, b) => {
        const dateA = new Date(a.created_at || a.start_date || 0);
        const dateB = new Date(b.created_at || b.start_date || 0);
        return dateB.getTime() - dateA.getTime();
      });
    } else if (sortOrder === "oldest") {
      events = [...events].sort((a, b) => {
        const dateA = new Date(a.created_at || a.start_date || 0);
        const dateB = new Date(b.created_at || b.start_date || 0);
        return dateA.getTime() - dateB.getTime();
      });
    }
  }
  
  // Обработчик изменения сортировки
  function handleSortChange(e) {
    sortOrder = e.target.value;
    sortEvents();
  }
  
  onMount(() => {
    loadEvents();
  });
</script>

<div class="page-container">
  <div class="container">
    <main>
      <div class="content-header">
        <h2 class="main-title">Конференции<br>и мероприятия</h2>
        
        <div class="filters">
          <div class="filter-group">
            <label>По новизне</label>
            <select class="filter-select" on:change={handleSortChange} bind:value={sortOrder}>
              <option value="default">По умолчанию</option>
              <option value="newest">Сначала новые</option>
              <option value="oldest">Сначала старые</option>
            </select>
          </div>
        </div>
      </div>

      {#if loading}
        <div class="loading">Загрузка событий...</div>
      {:else}
        <div class="events-list">
          {#each events as event}
            <div class="event-card">
              <div class="event-image">
                <img src={event.image} alt={event.title} onerror="this.src='/event1.png'" />
              </div>
              <div class="event-content">
                <div class="event-tag">{event.tag}</div>
                <h3 class="event-title">{event.title}</h3>
                {#if event.start_date && event.end_date}
                  <div class="event-dates">
                    {#if areSameDates(event.start_date, event.end_date)}
                      {formatDate(event.start_date)}
                    {:else}
                      {formatDate(event.start_date)} - {formatDate(event.end_date)}
                    {/if}
                  </div>
                {/if}
                <p class="event-description">{event.description}</p>
                
                {#if isAuthenticated && event.max_participants !== undefined}
                  <div class="participants-info">
                    <div class="participants-count">
                      Участники: {event.current_participants} из {event.max_participants}
                    </div>
                  </div>
                  
                  <div class="registration-container">
                    {#if event.is_registered}
                      <button 
                        class="unregister-button" 
                        on:click={() => handleUnregister(event.id)}
                        disabled={isRegistering && selectedEventId === event.id}
                      >
                        {isRegistering && selectedEventId === event.id ? 'Отмена регистрации...' : 'Отменить регистрацию'}
                      </button>
                    {:else if event.current_participants < event.max_participants}
                      <button 
                        class="register-button" 
                        on:click={() => handleRegister(event.id)}
                        disabled={isRegistering && selectedEventId === event.id}
                      >
                        {isRegistering && selectedEventId === event.id ? 'Регистрация...' : 'Зарегистрироваться'}
                      </button>
                    {:else}
                      <button class="register-button disabled" disabled>
                        Мест больше нет
                      </button>
                    {/if}
                  </div>
                {:else}
                  <div class="unauthorized-message">
                    <a href="/login?redirect=/afisha" class="login-button">Войдите, чтобы зарегистрироваться</a>
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </main>
  </div>
</div>

<style>
  @font-face {
    font-family: 'SF Pro Display';
    src: url('/font/SF-Pro-Display-Regular.otf') format('opentype');
    font-weight: 400;
    font-style: normal;
  }

  @font-face {
    font-family: 'SF Pro Display';
    src: url('/font/SF-Pro-Display-Medium.otf') format('opentype');
    font-weight: 500;
    font-style: normal;
  }

  @font-face {
    font-family: 'SF Pro Display';
    src: url('/font/SF-Pro-Display-Bold.otf') format('opentype');
    font-weight: 700;
    font-style: normal;
  }

  @font-face {
    font-family: 'SF Pro Display';
    src: url('/font/SF-Pro-Display-Light.otf') format('opentype');
    font-weight: 300;
    font-style: normal;
  }

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'SF Pro Display', Arial, sans-serif;
    background-color: #ffffff;
  }

  .page-container {
    width: 100%;
    background-color: #ffffff;
    min-height: 100vh;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Content Header */
  .content-header {
    margin: 40px 0;
  }

  .main-title {
    font-size: 42px;
    font-weight: 600;
    margin-bottom: 30px;
    line-height: 1.2;
    text-align: left;
  }

  /* Filters */
  .filters {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
    justify-content: flex-start;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .filter-group label {
    font-size: 16px;
    color: #666;
  }

  .filter-select {
    padding: 10px 15px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    background-color: #f5f5f5;
    width: 200px;
    font-family: 'SF Pro Display', Arial, sans-serif;
    font-size: 15px;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 16px;
  }

  /* Events List */
  .events-list {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-bottom: 60px;
  }

  .event-card {
    display: flex;
    background-color: #E4E4E4;
    border-radius: 20px;
    overflow: hidden;
  }

  .event-image {
    width: 270px;
    height: 270px;
    flex-shrink: 0;
    overflow: hidden;
    padding: 8px 0 8px 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
  }

  .event-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    max-width: 210px;
    max-height: 210px;
  }

  .event-content {
    flex: 1;
    padding: 30px;
    position: relative;
    min-height: 210px;
    display: flex;
    flex-direction: column;
    text-align: left;
  }

  .event-tag {
    display: inline-block;
    background-color: #1A3882;
    color: white;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 14px;
    margin-bottom: 15px;
    align-self: flex-start;
  }

  .event-title {
    font-size: 28px;
    font-weight: 600;
    margin: 0 0 5px 0;
    line-height: 1.3;
    text-align: left;
  }

  .event-dates {
    margin-bottom: 10px;
    color: #666;
    font-size: 16px;
  }

  .event-description {
    color: #444;
    line-height: 1.5;
    margin-top: 5px;
    margin-bottom: 20px;
    flex-grow: 1;
    font-size: 18px;
    text-align: left;
  }
  
  /* Participants info */
  .participants-info {
    margin-bottom: 15px;
    align-self: flex-start;
  }
  
  .participants-count {
    font-size: 16px;
    color: #777;
    text-align: left;
    margin-bottom: 10px;
  }
  
  .registration-container {
    display: flex;
    justify-content: flex-start;
  }
  
  .register-button, .unregister-button, .login-button {
    padding: 10px 24px;
    border-radius: 12px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    transition: background-color 0.2s;
    display: inline-block;
    text-align: center;
  }
  
  .register-button {
    background-color: #1A3882;
    color: white;
  }
  
  .register-button:hover {
    background-color: #132a62;
  }
  
  .register-button.disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .unregister-button {
    background-color: #f0f0f0;
    color: #cc0000;
    border: 1px solid #cc0000;
  }
  
  .unregister-button:hover {
    background-color: #ffebeb;
  }
  
  .unauthorized-message {
    display: flex;
    justify-content: flex-start;
  }
  
  .login-button {
    background-color: #f5f5f5;
    color: #1A3882;
    border: 1px solid #1A3882;
    text-decoration: none;
  }
  
  .login-button:hover {
    background-color: #e8e8e8;
  }

  /* Notifications */
  .loading {
    padding: 15px;
    margin-bottom: 30px;
    border-radius: 8px;
    position: relative;
    text-align: left;
    font-size: 18px;
    background-color: #f5f5f5;
  }
  
  @media (max-width: 768px) {
    .event-card {
      flex-direction: column;
    }

    .event-image {
      width: 100%;
      height: auto;
      aspect-ratio: 1/1;
      padding: 30px;
    }
    
    .event-image img {
      max-width: 100%;
      max-height: 100%;
    }
    
    .filters {
      flex-direction: column;
      gap: 15px;
    }
    
    .filter-select {
      width: 100%;
    }
    
    .event-content {
      padding: 20px;
    }
    
    .main-title {
      font-size: 32px;
    }
    
    .event-title {
      font-size: 24px;
    }
    
    .registration-container {
      justify-content: flex-start;
    }
  }
</style> 