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
      image: "/classroom1.jpg",
      capacity: 70,
      description: "Просторная, современная аудитория вместительностью 70 человек, отлично подойдёт для форумов и различных митапов, аудитория также очень просторная, стулья для зрителей предоставляются в ограниченном количестве"
    },
    {
      id: 2,
      number: "305",
      building: "А",
      title: "Аудитория 305, Корпус А",
      image: "/classroom2.jpg",
      capacity: 50,
      description: "Просторная, современная аудитория вместительностью 50 человек, отлично подойдёт для форумов и различных митапов, аудитория также очень просторная, стулья для зрителей предоставляются в ограниченном количестве"
    }
  ];
  
  let selectedClassroomNumber = "Любой";
  let selectedBuilding = "Любой";
  let currentClassroomIndex = 0;
  
  function nextClassroom() {
    if (currentClassroomIndex < filteredClassrooms.length - 1) {
      currentClassroomIndex++;
    }
  }
  
  function prevClassroom() {
    if (currentClassroomIndex > 0) {
      currentClassroomIndex--;
    }
  }
  
  function bookClassroom(id: number) {
    alert("Функционал бронирования будет доступен в ближайшее время");
  }
  
  function handleImageError(event: Event) {
    const imgElement = event.target as HTMLImageElement;
    imgElement.src = '/placeholder-classroom.jpg';
  }
  
  $: filteredClassrooms = classrooms.filter(classroom => {
    const matchesNumber = selectedClassroomNumber === "Любой" || classroom.number === selectedClassroomNumber;
    const matchesBuilding = selectedBuilding === "Любой" || classroom.building === selectedBuilding;
    return matchesNumber && matchesBuilding;
  });
  
  $: currentClassroom = filteredClassrooms[currentClassroomIndex] || null;
  
  onMount(() => {
    // Any initialization code can go here
  });
</script>

<div class="booking-page">
  <div class="container">
    <header>
      <h1 class="page-title">Бронирование<br>аудитории</h1>
    </header>
    
    <div class="filters">
      <div class="filter-group">
        <label for="classroom-number">Номер аудитории</label>
        <div class="select-wrapper">
          <select id="classroom-number" bind:value={selectedClassroomNumber}>
            <option value="Любой">Любой</option>
            {#each [...new Set(classrooms.map(c => c.number))] as number}
              <option value={number}>{number}</option>
            {/each}
          </select>
        </div>
      </div>
      
      <div class="filter-group">
        <label for="building-number">Номер корпуса</label>
        <div class="select-wrapper">
          <select id="building-number" bind:value={selectedBuilding}>
            <option value="Любой">Любой</option>
            {#each [...new Set(classrooms.map(c => c.building))] as building}
              <option value={building}>{building}</option>
            {/each}
          </select>
        </div>
      </div>
    </div>
    
    {#if filteredClassrooms.length > 0 && currentClassroom}
      <div class="classrooms-container">
        <div class="classroom-card">
          <div class="classroom-image">
            <img src={currentClassroom.image} alt={currentClassroom.title} on:error={handleImageError}>
            
            <!-- Navigation arrows -->
            <button class="nav-arrow left-arrow" on:click={prevClassroom} disabled={currentClassroomIndex === 0}>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="12" fill="white" fill-opacity="0.8"/>
                <path d="M15 18L9 12L15 6" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button class="nav-arrow right-arrow" on:click={nextClassroom} disabled={currentClassroomIndex === filteredClassrooms.length - 1}>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="12" fill="white" fill-opacity="0.8"/>
                <path d="M9 18L15 12L9 6" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          
          <div class="classroom-details">
            <h2>{currentClassroom.title}</h2>
            <p class="classroom-description">{currentClassroom.description}</p>
            
            <button class="book-button" on:click={() => bookClassroom(currentClassroom.id)}>
              Забронировать аудиторию
            </button>
          </div>
        </div>
      </div>
    {:else}
      <div class="no-results">
        <p>Нет доступных аудиторий по указанным критериям</p>
      </div>
    {/if}
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
    z-index: 1;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  /* Header styles */
  header {
    margin-bottom: 40px;
  }

  .page-title {
    font-size: 36px;
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 30px;
    color: #333;
  }

  /* Filters */
  .filters {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
    flex-wrap: wrap;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 220px;
  }

  .filter-group label {
    font-size: 16px;
    color: #333;
    font-weight: 500;
  }

  .select-wrapper {
    position: relative;
  }

  select {
    width: 100%;
    padding: 12px 15px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: white;
    appearance: none;
    font-family: 'SF Pro Display', Arial, sans-serif;
    cursor: pointer;
  }

  .select-wrapper::after {
    content: '';
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    width: 10px;
    height: 10px;
    border-right: 2px solid #666;
    border-bottom: 2px solid #666;
    transform: translateY(-70%) rotate(45deg);
    pointer-events: none;
  }

  /* Classroom Card */
  .classrooms-container {
    margin-top: 30px;
  }

  .classroom-card {
    display: flex;
    background-color: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
  }

  .classroom-image {
    position: relative;
    width: 40%;
    min-height: 300px;
    background-color: #f5f5f5;
  }

  .classroom-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .classroom-details {
    padding: 30px;
    width: 60%;
  }

  .classroom-details h2 {
    font-size: 24px;
    margin-bottom: 15px;
    color: #333;
  }

  .classroom-description {
    margin-bottom: 30px;
    line-height: 1.6;
    color: #555;
  }

  .book-button {
    background-color: #294380;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .book-button:hover {
    background-color: #1A3070;
  }

  /* Navigation Arrows */
  .nav-arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    background: none;
    border: none;
    cursor: pointer;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  .nav-arrow svg {
    width: 100%;
    height: 100%;
  }

  .left-arrow {
    left: 15px;
  }

  .right-arrow {
    right: 15px;
  }

  .nav-arrow:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .no-results {
    padding: 40px;
    text-align: center;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .no-results p {
    font-size: 18px;
    color: #666;
  }

  /* Responsive */
  @media (max-width: 768px) {
    .classroom-card {
      flex-direction: column;
    }

    .classroom-image,
    .classroom-details {
      width: 100%;
    }

    .classroom-image {
      height: 200px;
    }
  }
</style> 