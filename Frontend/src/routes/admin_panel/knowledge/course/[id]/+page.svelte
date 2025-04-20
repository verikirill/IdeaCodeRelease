<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  
  // Получаем ID курса из параметров
  const courseId = $page.params.id;
  
  // Названия курсов с индексацией по строке
  const courseTitles: Record<string, string> = {
    '1': '2025. Физика. Лабораторные работы. Механика',
    '2': 'История России',
    '3': 'Компьютерная инженерная графика',
    '4': 'Введение в специальность 2025',
    '5': 'Вычислительные машины, системы и сети',
    '6': 'Программирование и алгоритмизация',
    '7': 'Персональная эффективность',
    '8': 'Основы дискретной математики'
  };
  
  // Текущее название курса
  let courseTitle = courseTitles[courseId] || 'Курс';
  
  // Данные лекций
  let lectures = [
    {
      id: 1,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (1).png'
    },
    {
      id: 2,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (2).png'
    },
    {
      id: 3,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (3).png'
    },
    {
      id: 4,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (4).png'
    },
    {
      id: 5,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (5).png'
    },
    {
      id: 6,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (6).png'
    },
    {
      id: 7,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (7).png'
    },
    {
      id: 8,
      title: 'Лекция 1. Основы алгоритмизации и программирования',
      image: '/admin/disc (8).png'
    }
  ];
  
  let selectedFilter = 'Любой';
  
  function downloadPdf(lectureId: number, event: Event): void {
    event.stopPropagation();
    console.log(`Скачивание PDF для лекции ${lectureId}`);
    // Здесь будет логика скачивания PDF
  }
  
  function viewLecture(lectureId: number, event: Event): void {
    event.stopPropagation();
    console.log(`Просмотр лекции ${lectureId}`);
    // Здесь будет логика просмотра лекции
  }
  
  function addLecture(): void {
    console.log('Добавление нового конспекта');
    // Логика добавления нового конспекта
  }
  
  function goBack(): void {
    goto('/admin_panel/knowledge');
  }
  
  onMount(() => {
    // Инициализация при загрузке страницы
  });
</script>

<div class="course-page">
  <div class="container">
    <header>
      <h1>{courseTitle}</h1>
    </header>
    
    <div class="search-section">
      <div class="search-container">
        <p class="search-label">Поиск по теме</p>
        <div class="select-container">
          <select bind:value={selectedFilter} class="filter-select">
            <option value="Любой">Любой</option>
          </select>
        </div>
      </div>
      
      <button class="add-lecture-button" on:click={addLecture}>
        Добавить конспект
        <span class="plus-icon">+</span>
      </button>
    </div>
    
    <div class="lectures-grid">
      {#each lectures as lecture (lecture.id)}
        <div class="lecture-card">
          <div class="card-image-container">
            <img src={lecture.image} alt={lecture.title} class="lecture-image" />
          </div>
          <div class="lecture-info">
            <p class="lecture-title">{lecture.title}</p>
          </div>
          <div class="lecture-actions">
            <button class="download-button" on:click={(e) => downloadPdf(lecture.id, e)}>
              Скачать Pdf
              <span class="download-icon">↓</span>
            </button>
            <button class="view-button" on:click={(e) => viewLecture(lecture.id, e)}>
              Посмотреть
              <span class="view-icon">👁</span>
            </button>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .course-page {
    width: 100%;
    min-height: 100vh;
    padding: 20px 0;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  header {
    margin: 20px 0;
  }
  
  h1 {
    font-size: 32px;
    color: #333;
    margin: 0;
    font-weight: 600;
  }
  
  /* Поиск и кнопка добавления */
  .search-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 30px;
  }
  
  .search-container {
    max-width: 400px;
  }
  
  .search-label {
    font-size: 16px;
    color: #333;
    margin-bottom: 10px;
  }
  
  .select-container {
    position: relative;
  }
  
  .filter-select {
    width: 100%;
    padding: 12px 15px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: white;
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
  }
  
  .select-container::after {
    content: "▼";
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
    color: #666;
    font-size: 14px;
  }
  
  .add-lecture-button {
    background-color: #1A3882;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .plus-icon {
    font-size: 20px;
  }
  
  /* Сетка лекций */
  .lectures-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  
  .lecture-card {
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
  }
  
  .card-image-container {
    width: 100%;
    height: 200px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f5f5f5;
    padding: 0;
  }
  
  .lecture-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .lecture-info {
    padding: 15px;
  }
  
  .lecture-title {
    font-size: 16px;
    font-weight: 500;
    color: #333;
    margin: 0;
  }
  
  .lecture-actions {
    display: flex;
    justify-content: space-between;
    padding: 0 15px 15px;
    gap: 10px;
  }
  
  .download-button, .view-button {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
  }
  
  .download-button {
    background-color: #f5f5f5;
    color: #333;
  }
  
  .view-button {
    background-color: #1A3882;
    color: white;
  }
  
  .download-icon, .view-icon {
    font-size: 16px;
  }
  
  @media (max-width: 900px) {
    .lectures-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (max-width: 600px) {
    .lectures-grid {
      grid-template-columns: 1fr;
    }
    
    .search-section {
      flex-direction: column;
      align-items: stretch;
      gap: 20px;
    }
    
    .lecture-actions {
      flex-direction: column;
    }
  }
</style> 