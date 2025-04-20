<script lang="ts">
  import { onMount } from 'svelte';
  import { getUserGroup, getUserSchedule, getUserScheduleByDay } from '$lib/services/timetable';
  import { authStore } from '$lib/services/auth';
  import { goto } from '$app/navigation';
  import { fade, slide, scale, fly } from 'svelte/transition';
  import { quintOut, cubicOut } from 'svelte/easing';
  import type { Group, Lesson } from '$lib/services/timetable';
  
  // Активный день недели (по умолчанию - сегодняшний день)
  const today = new Date().getDay();
  // Преобразуем день недели из JavaScript (0 - воскр, 1 - пн, ...) в формат бэкенда (0 - пн, 1 - вт, ...)
  let activeDay = today === 0 ? 6 : today - 1; 
  
  // Дни недели
  const weekDays = [
    { id: 0, name: 'Пн' },
    { id: 1, name: 'Вт' },
    { id: 2, name: 'Ср' },
    { id: 3, name: 'Чт' },
    { id: 4, name: 'Пт' },
    { id: 5, name: 'Сб' },
    { id: 6, name: 'Вс' }
  ];
  
  // Данные для расписания
  let isLoading = true;
  let error: string | null = null;
  let selectedGroup: Group | null = null;
  let schedule: Lesson[] = [];
  let filteredSchedule: Lesson[] = [];
  let isWeekTypeUpper = determineWeekType(); // true - верхняя неделя, false - нижняя неделя
  let scheduleVisible = false;
  
  // Функция определения типа недели (верхняя/нижняя)
  function determineWeekType(): boolean {
    const now = new Date();
    const weekNumber = now.getFullYear() * 100 + Math.ceil((now.getTime() - new Date(now.getFullYear(), 0, 1).getTime() + 
                        ((new Date(now.getFullYear(), 0, 1).getDay() + 6) % 7) * 86400000) / 
                        (86400000 * 7));
    return weekNumber % 2 === 1; // Нечётная неделя - верхняя, чётная - нижняя (как в бэкенде)
  }
  
  // Переключение активного дня
  function setActiveDay(day: number) {
    activeDay = day;
    filterScheduleByDay();
  }
  
  // Переключение типа недели
  function toggleWeekType() {
    isWeekTypeUpper = !isWeekTypeUpper;
    filterScheduleByDay();
  }
  
  // Фильтрация расписания по текущему дню
  function filterScheduleByDay() {
    console.log("Фильтрация расписания:", {
      activeDay,
      isWeekTypeUpper,
      schedule: schedule.length,
    });
    
    filteredSchedule = schedule.filter(lesson => {
      if (lesson.weekday !== activeDay) return false;
      
      if (isWeekTypeUpper) {
        return lesson.odd_week; // Для верхней недели используем odd_week как в бэкенде
      } else {
        return lesson.even_week; // Для нижней недели используем even_week как в бэкенде
      }
    }).sort((a, b) => a.number - b.number);
    
    console.log("Отфильтрованное расписание:", filteredSchedule);
    
    // Проверка наличия данных о местах проведения занятий
    if (filteredSchedule.length > 0) {
      filteredSchedule.forEach(lesson => {
        console.log(`Информация о местах проведения для ${lesson.subject.name}:`, lesson.places);
      });
    }
  }
  
  // Загрузка данных
  async function loadSchedule() {
    try {
      isLoading = true;
      error = null;
      
      // Проверяем аутентификацию
      let isAuthenticated = false;
      authStore.isAuthenticated.subscribe(value => {
        isAuthenticated = value;
      })();
      
      if (!isAuthenticated) {
        goto('/login?redirect=/schedule');
        return;
      }
      
      // Получаем выбранную группу
      selectedGroup = await getUserGroup();
      console.log("Выбранная группа:", selectedGroup);
      
      if (!selectedGroup) {
        error = 'Вы не выбрали группу. Перейдите в профиль, чтобы выбрать группу для просмотра расписания.';
        isLoading = false;
        return;
      }
      
      // Получаем расписание
      const weekType = isWeekTypeUpper ? 'upper' : 'lower';
      schedule = await getUserScheduleByDay(activeDay, weekType);
      console.log("Загруженное расписание:", schedule);
      
      if (!schedule || !Array.isArray(schedule) || schedule.length === 0) {
        console.log("Расписание пустое или в неверном формате, пробуем получить полное расписание");
        // Если не получили расписание через getUserScheduleByDay, пробуем через getUserSchedule
        const fullSchedule = await getUserSchedule();
        if (fullSchedule && Array.isArray(fullSchedule)) {
          schedule = fullSchedule;
        }
      }
      
      // Фильтруем по активному дню
      filterScheduleByDay();
      
    } catch (err) {
      console.error('Ошибка при загрузке расписания:', err);
      error = 'Произошла ошибка при загрузке расписания. Пожалуйста, попробуйте позже.';
    } finally {
      isLoading = false;
    }
  }
  
  // Форматирование названия предмета
  function formatSubjectName(name: string): string {
    const maxLength = 40;
    if (name.length <= maxLength) return name;
    return name.substring(0, maxLength) + '...';
  }
  
  // Переход на страницу профиля
  function goToProfile() {
    goto('/account');
  }
  
  onMount(() => {
    loadSchedule();
    
    // Set up intersection observer for schedule contents
    const scheduleObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          scheduleVisible = true;
          scheduleObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    
    // Observe schedule container
    const scheduleContainer = document.querySelector('.schedule-container');
    if (scheduleContainer) {
      scheduleObserver.observe(scheduleContainer);
    }
  });
</script>

<div class="schedule-content">
  <!-- Содержимое страницы расписания -->
  <div class="schedule-container">
    {#if scheduleVisible}
      <h1 class="title" in:fly={{ y: 20, duration: 500, delay: 0, easing: cubicOut }}>Расписание</h1>
      
      {#if selectedGroup}
        <p class="subtitle" in:fly={{ y: 20, duration: 500, delay: 100, easing: cubicOut }}>Группа {selectedGroup.number} {selectedGroup.name ? `(${selectedGroup.name})` : ''}</p>
      {:else}
        <p class="subtitle" in:fly={{ y: 20, duration: 500, delay: 100, easing: cubicOut }}>Выберите группу в настройках профиля</p>
      {/if}
      
      <!-- Дни недели -->
      <div class="controls" in:fly={{ y: 20, duration: 500, delay: 200, easing: cubicOut }}>
        <div class="weekdays">
          {#each weekDays as day, i}
            <button 
              class="day-button {day.id === activeDay ? 'active' : ''}" 
              on:click={() => setActiveDay(day.id)}
              in:fly={{ y: 15, duration: 300, delay: 250 + (i * 50), easing: cubicOut }}
            >
              {day.name}
            </button>
          {/each}
        </div>
        
        <div class="week-type-toggle" in:fly={{ y: 15, duration: 300, delay: 600, easing: cubicOut }}>
          <button 
            class="week-type-button {isWeekTypeUpper ? 'active' : ''}" 
            on:click={toggleWeekType}
          >
            {isWeekTypeUpper ? 'Верхняя неделя' : 'Нижняя неделя'}
          </button>
        </div>
      </div>
      
      <!-- Содержимое расписания -->
      {#if isLoading}
        <div class="loading" in:fade={{ duration: 200 }}>Загрузка расписания...</div>
      {:else if error}
        <div class="error" in:fly={{ y: 20, duration: 500, delay: 700, easing: cubicOut }}>
          <p>{error}</p>
          <button class="profile-button" on:click={goToProfile}>Перейти в профиль</button>
        </div>
      {:else if filteredSchedule.length === 0}
        <div class="empty-schedule" in:fly={{ y: 20, duration: 500, delay: 700, easing: cubicOut }}>
          <p>На выбранный день занятий нет</p>
        </div>
      {:else}
        <!-- Таблица с расписанием -->
        <div class="schedule-table" in:fly={{ y: 20, duration: 500, delay: 700, easing: cubicOut }}>
          {#each filteredSchedule as lesson, i}
            <div 
              class="schedule-row" 
              in:fly={{ y: 15, duration: 300, delay: 800 + (i * 100), easing: cubicOut }}
            >
              <div class="time">{lesson.start_time} - {lesson.end_time}</div>
              <div class="subject">{formatSubjectName(lesson.subject.name)}</div>
              <div class="location">
                {#if lesson.places && lesson.places.length > 0}
                  <span class="location-label">Кабинет:</span>
                  {lesson.places.map(place => place.name).join(', ')}
                {:else}
                  -
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    {/if}
  </div>
</div>

<style>
  /* Стили для страницы и фона */
  .schedule-page {
    display: none; /* Hiding the page-specific background */
  }
  
  .schedule-content {
    position: relative;
    min-height: 100vh;
    padding-bottom: 40px;
    z-index: 1;
  }
  
  /* Стили для расписания */
  .schedule-container {
    padding: 20px;
    max-width: 900px;
    margin: 0 auto;
  }
  
  .title {
    font-size: 32px;
    color: #333;
    margin: 0 0 5px 0;
  }
  
  .subtitle {
    font-size: 18px;
    color: #666;
    margin: 0 0 30px 0;
  }
  
  /* Контролы */
  .controls {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 30px;
  }
  
  /* Дни недели */
  .weekdays {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 5px;
  }
  
  .day-button {
    width: 80px;
    height: 80px;
    border-radius: 10px;
    border: none;
    background-color: white;
    color: #294380;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    flex-shrink: 0;
  }
  
  .day-button:hover {
    background-color: #f5f7fa;
  }
  
  .day-button.active {
    background-color: #294380;
    color: white;
  }
  
  /* Переключатель типа недели */
  .week-type-toggle {
    display: flex;
    justify-content: flex-start;
    padding-left: 0;
  }
  
  .week-type-button {
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #294380;
    background-color: white;
    color: #294380;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 180px;
  }
  
  .week-type-button:hover {
    background-color: #f5f7fa;
  }
  
  .week-type-button.active {
    background-color: #294380;
    color: white;
  }
  
  /* Состояния загрузки и ошибки */
  .loading, .error, .empty-schedule {
    background-color: white;
    border-radius: 10px;
    padding: 40px 20px;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  .loading {
    color: #666;
  }
  
  .error {
    color: #d32f2f;
  }
  
  .empty-schedule {
    color: #666;
  }
  
  .profile-button {
    margin-top: 15px;
    padding: 10px 20px;
    border-radius: 5px;
    background-color: #294380;
    color: white;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .profile-button:hover {
    background-color: #1a2a50;
  }
  
  /* Таблица расписания */
  .schedule-table {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .schedule-row {
    display: flex;
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
  }
  
  .schedule-row:hover {
    background-color: #f9fafc;
  }
  
  .time {
    width: 150px;
    font-weight: bold;
    color: #333;
  }
  
  .subject {
    flex: 1;
    color: #444;
  }
  
  .location {
    width: 150px;
    text-align: right;
    color: #666;
  }
  
  .location-label {
    display: inline-block;
    margin-right: 5px;
    font-weight: bold;
    color: #294380;
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .weekdays {
      flex-wrap: wrap;
      justify-content: center;
    }
    
    .week-type-toggle {
      justify-content: center;
      padding-left: 0;
    }
    
    .schedule-row {
      flex-direction: column;
      gap: 10px;
    }
    
    .time, .subject, .location {
      width: 100%;
      text-align: left;
    }
    
    .location {
      border-top: 1px solid #eee;
      padding-top: 8px;
      margin-top: 5px;
    }
  }
</style>