<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let selectedFilter = 'Любой';
  let courses = [
    {
      id: 1,
      title: '2025. Физика. Лабораторные работы. Механика',
      image: '/admin/disc (1).png',
    },
    {
      id: 2,
      title: 'История России',
      image: '/admin/disc (2).png',
    },
    {
      id: 3,
      title: 'Компьютерная инженерная графика',
      image: '/admin/disc (3).png',
    },
    {
      id: 4,
      title: 'Введение в специальность 2025',
      image: '/admin/disc (4).png',
    },
    {
      id: 5,
      title: 'Вычислительные машины, системы и сети',
      image: '/admin/disc (5).png',
    },
    {
      id: 6,
      title: 'Программирование и алгоритмизация',
      image: '/admin/disc (6).png',
    },
    {
      id: 7,
      title: 'Персональная эффективность',
      image: '/admin/disc (7).png',
    },
    {
      id: 8,
      title: 'Основы дискретной математики',
      image: '/admin/disc (8).png',
    }
  ];
  
  function handleFilterChange(event: Event): void {
    selectedFilter = (event.target as HTMLSelectElement).value;
    // Здесь можно добавить фильтрацию по выбранному значению
  }
  
  function handleCardClick(id: number): void {
    console.log(`Открыт курс с ID: ${id}`);
    // Переход на страницу курса
    goto(`/admin_panel/knowledge/course/${id}`);
  }
  
  onMount(() => {
    // Инициализация при загрузке страницы
  });
</script>

<div class="knowledge-admin-page">
  <div class="container">
    <header>
      <h1>Лекции и конспекты</h1>
    </header>
    
    <section class="search-section">
      <div class="search-container">
        <p class="search-label">Поиск по названию</p>
        <div class="select-container">
          <select bind:value={selectedFilter} on:change={handleFilterChange} class="filter-select">
            <option value="Любой">Любой</option>
            <option value="Физика">Физика</option>
            <option value="История">История</option>
            <option value="Программирование">Программирование</option>
            <option value="Математика">Математика</option>
          </select>
        </div>
      </div>
    </section>
    
    <section class="courses-grid">
      {#each courses as course (course.id)}
        <div class="course-card" on:click={() => handleCardClick(course.id)}>
          <img src={course.image} alt={course.title} class="card-image" />
          <div class="card-title">{course.title}</div>
        </div>
      {/each}
    </section>
  </div>
</div>

<style>
  .knowledge-admin-page {
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
    margin: 40px 0 20px;
  }
  
  h1 {
    font-size: 32px;
    color: #333;
    margin: 0;
    font-weight: 600;
  }
  
  /* Поиск и фильтры */
  .search-section {
    margin: 30px 0;
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
  
  /* Сетка курсов */
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-top: 40px;
  }
  
  .course-card {
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    padding: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    height: 230px;
  }
  
  .course-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
  
  .card-image {
    width: 230px;
    height: 200px;
    object-fit: contain;
    margin-bottom: 10px;
    flex-grow: 1;
  }
  
  .card-title {
    font-size: 15px;
    font-weight: 500;
    color: #333;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  @media (max-width: 900px) {
    .courses-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (max-width: 600px) {
    .courses-grid {
      grid-template-columns: 1fr;
    }
  }
</style> 