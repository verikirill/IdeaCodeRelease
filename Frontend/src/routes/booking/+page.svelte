<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  
  interface Classroom {
    id: number;
    number: string;
    building: string;
    title: string;
    image: string;
    capacity: number;
    description: string;
  }
  
  let classrooms: Classroom[] = [
    {
      id: 1,
      number: "512",
      building: "Б",
      title: "Аудитория 512, Корпус Б",
      image: "/audit (1).png",
      capacity: 70,
      description: "Просторная, современная аудитория вместительностью 70 человек, отлично подойдёт для форумов и различных митапов, аудитория также очень просторная, стулья для зрителей предоставляются в ограниченном количестве"
    },
    {
      id: 2,
      number: "305",
      building: "А",
      title: "Аудитория 305, Корпус А",
      image: "/audit (2).png",
      capacity: 50,
      description: "Просторная, современная аудитория вместительностью 50 человек, отлично подойдёт для форумов и различных митапов, аудитория также очень просторная, стулья для зрителей предоставляются в ограниченном количестве"
    },
    {
      id: 3,
      number: "401",
      building: "В",
      title: "Аудитория 401, Корпус В",
      image: "/audit (3).png",
      capacity: 60,
      description: "Просторная, современная аудитория вместительностью 60 человек, отлично подойдёт для форумов и различных митапов, аудитория также очень просторная, стулья для зрителей предоставляются в ограниченном количестве"
    }
  ];
  
  let selectedTopic = "Любой";
  
  function bookClassroom(id: number) {
    alert("Функционал бронирования будет доступен в ближайшее время");
  }
  
  function handleImageError(event: Event) {
    const imgElement = event.target as HTMLImageElement;
    imgElement.src = '/placeholder-classroom.jpg';
  }
  
  $: filteredClassrooms = classrooms;
  
  onMount(() => {
    // Any initialization code can go here
  });
</script>

<div class="booking-page">
  <div class="container">
    <div class="page-header">
      <h1>Бронирование аудитории</h1>
      
      <div class="search-create">
        <div class="search">
          <label for="topic-select">Поиск по теме</label>
          <div class="select-wrapper">
            <select id="topic-select" bind:value={selectedTopic}>
              <option value="Любой">Любой</option>
            </select>
          </div>
        </div>
        
        <button class="create-button">
          Создать заметку
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 3V13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M3 8H13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
    
    <div class="classrooms-list">
      {#each filteredClassrooms as classroom}
        <div class="classroom-card">
          <div class="classroom-image-container">
            <button class="card-nav-arrow left-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 18L9 12L15 6" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            
            <div class="classroom-image">
              <img src={classroom.image} alt={classroom.title} on:error={handleImageError}>
            </div>
            
            <button class="card-nav-arrow right-arrow">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 18L15 12L9 6" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          
          <div class="classroom-info">
            <h2>{classroom.title}</h2>
            <p class="classroom-description">
              {classroom.description}
            </p>
            
            <button class="book-button" on:click={() => bookClassroom(classroom.id)}>
              Забронировать аудиторию
            </button>
          </div>
        </div>
      {/each}
    </div>
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

  .booking-page {
    position: relative;
    width: 100%;
    min-height: 100vh;
    font-family: 'SF Pro Display', Arial, sans-serif;
  }

  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }

  .page-header {
    margin-bottom: 20px;
    padding-top: 10px;
  }

  h1 {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 16px;
    color: #333;
  }

  .search-create {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 20px;
  }

  .search {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .search label {
    font-size: 14px;
    color: #333;
  }

  .select-wrapper {
    position: relative;
    width: 180px;
  }

  select {
    width: 100%;
    padding: 8px 12px;
    border-radius: 16px;
    border: none;
    appearance: none;
    background-color: white;
    font-family: 'SF Pro Display', Arial, sans-serif;
    font-size: 14px;
  }

  .create-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: #294380;
    color: white;
    border: none;
    border-radius: 16px;
    padding: 10px 16px;
    font-size: 14px;
    cursor: pointer;
  }

  .classrooms-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .classroom-card {
    display: flex;
    background-color: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .classroom-image-container {
    position: relative;
    width: 200px;
    min-width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    padding-left: 30px;
  }

  .classroom-image {
    width: 180px;
    height: 180px;
    overflow: hidden;
  }

  .classroom-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10%;
  }

  .card-nav-arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    border: none;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 2;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .left-arrow {
    left: 5px;
  }

  .right-arrow {
    right: -16px;
  }

  .classroom-info {
    padding: 20px;
    padding-left: 35px;
    display: flex;
    flex-direction: column;
  }

  .classroom-info h2 {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 10px;
    color: #333;
  }

  .classroom-description {
    font-size: 14px;
    line-height: 1.5;
    color: #333;
    margin-bottom: 20px;
    flex-grow: 1;
  }

  .book-button {
    align-self: flex-start;
    background-color: #294380;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .book-button:hover {
    background-color: #1A3070;
  }

  @media (max-width: 768px) {
    .classroom-card {
      flex-direction: column;
    }

    .classroom-image-container {
      width: 100%;
      height: 200px;
    }

    .search-create {
      flex-direction: column;
      gap: 16px;
      align-items: flex-start;
    }

    .select-wrapper {
      width: 100%;
    }

    .create-button {
      width: 100%;
      justify-content: center;
    }
  }
</style> 