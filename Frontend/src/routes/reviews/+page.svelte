<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto, afterNavigate } from '$app/navigation';
  import { fade, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  // Prevent auto-redirection
  let redirectAttempted = false;

  afterNavigate(() => {
    // Set flag after successful navigation to this page
    redirectAttempted = true;
  });

  interface Teacher {
    id: number;
    name: string;
    description: string;
    rating: number;
    reviewCount: number;
    image: string;
  }
  
  let teachers: Teacher[] = [
    {
      id: 1,
      name: "Имя преподавателя",
      description: "Краткое описание предмета и особенностей преподавателя",
      rating: 5,
      reviewCount: 3,
      image: '/avatar.png'
    },
    {
      id: 2,
      name: "Имя преподавателя",
      description: "Краткое описание предмета и особенностей преподавателя",
      rating: 4,
      reviewCount: 7,
      image: '/avatar.png'
    },
    {
      id: 3,
      name: "Имя преподавателя",
      description: "Краткое описание предмета и особенностей преподавателя",
      rating: 3,
      reviewCount: 5,
      image: '/avatar.png'
    }
  ];
  
  let selectedRating = "Любой";
  let searchQuery = "";
  
  let teachersVisible = true; // Set to true by default to ensure teachers are always visible
  
  function viewTeacherReviews(teacher: Teacher): void {
    // Functionality to display reviews for selected teacher
    console.log(`Viewing reviews for ${teacher.name}`);
    alert(`Отзывы для ${teacher.name} будут доступны в ближайшее время`);
  }
  
  function handleImageError(event: Event): void {
    // Fallback if image fails to load
    const target = event.target as HTMLImageElement;
    target.src = '/avatar.png';
  }
  
  onMount(() => {
    // Simple initialization
    teachersVisible = true;
    
    // Check for unintended navigation
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (!redirectAttempted) {
        // This will prevent redirects from this page
        e.preventDefault();
        e.returnValue = '';
        return '';
      }
    };
    
    window.addEventListener('beforeunload', handleBeforeUnload);
    
    // Cancel any pending redirects
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  });
</script>

<svelte:head>
  <title>Отзывы о преподавателях</title>
</svelte:head>

<div class="reviews-page"></div>
<div class="reviews-content">
  <div class="container">
    <main>
      <div class="reviews-header">
        <h1>Отзывы о преподавателях</h1>
      </div>

      <div class="filters">
        <div class="filter-group">
          <label>По баллам</label>
          <select bind:value={selectedRating} class="filter-select">
            <option>Любой</option>
            <option>5 звезд</option>
            <option>4+ звезд</option>
            <option>3+ звезд</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>Искать преподавателя</label>
          <select bind:value={searchQuery} class="filter-select">
            <option>Любой</option>
            <!-- Additional options would be populated dynamically -->
          </select>
        </div>
      </div>

      <div class="teachers-list">
        {#each teachers as teacher, i}
          <div class="teacher-card">
            <div class="teacher-photo">
              <img src={teacher.image} alt={teacher.name} on:error={handleImageError} />
            </div>
            
            <div class="teacher-info">
              <div class="rating">
                {#each Array(5) as _, i}
                  <span class="star">{i < teacher.rating ? '★' : '☆'}</span>
                {/each}
              </div>
              
              <h2 class="teacher-name">{teacher.name}</h2>
              <p class="teacher-description">{teacher.description}</p>
              
              <div class="review-meta">
                <span class="review-count">
                  <span class="icon">📝</span> {teacher.reviewCount} {teacher.reviewCount === 1 ? 'отзыв' : (teacher.reviewCount < 5 ? 'отзыва' : 'отзывов')}
                </span>
              </div>
              
              <button class="view-reviews" on:click={() => viewTeacherReviews(teacher)}>
                Читать отзывы
              </button>
            </div>
          </div>
        {/each}
      </div>
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
  }

  /* Page background */
  .reviews-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #ededed;
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    z-index: -1;
  }
  
  .reviews-content {
    position: relative;
    min-height: 100vh;
    z-index: 1;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Reviews Header */
  .reviews-header {
    margin: 40px 0;
    text-align: center;
  }

  .reviews-header h1 {
    font-size: 32px;
    margin-bottom: 10px;
    color: #333;
  }

  /* Filters */
  .filters {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .filter-group label {
    font-size: 14px;
    color: #666;
  }

  .filter-select {
    padding: 10px 15px;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #fff;
    font-family: 'SF Pro Display', Arial, sans-serif;
    min-width: 200px;
  }

  /* Teachers List */
  .teachers-list {
    display: flex;
    flex-direction: column;
    gap: 30px;
    max-width: 800px;
    margin: 0 auto;
  }

  .teacher-card {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    display: flex;
    gap: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  }

  .teacher-photo {
    width: 120px;
    height: 150px;
    overflow: hidden;
    border-radius: 10px;
    flex-shrink: 0;
  }

  .teacher-photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .teacher-info {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .rating {
    display: flex;
    gap: 2px;
    margin-bottom: 10px;
  }

  .star {
    color: #1A3882;
    font-size: 24px;
  }

  .teacher-name {
    font-size: 20px;
    margin: 0 0 10px 0;
    color: #333;
  }

  .teacher-description {
    margin: 0 0 15px 0;
    color: #666;
    line-height: 1.4;
  }

  .review-meta {
    margin-bottom: 15px;
    font-size: 14px;
    color: #888;
    display: flex;
    align-items: center;
  }

  .review-count {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .icon {
    font-size: 18px;
    display: flex;
    align-items: center;
  }

  .view-reviews {
    background-color: #1A3882;
    border: none;
    border-radius: 12px;
    padding: 10px 0;
    width: 100%;
    max-width: 200px;
    cursor: pointer;
    font-size: 14px;
    color: #fff;
    text-align: center;
    font-family: 'SF Pro Display', Arial, sans-serif;
  }

  @media (max-width: 768px) {
    .teacher-card {
      flex-direction: column;
      align-items: center;
    }
    
    .teacher-photo {
      width: 100px;
      height: 130px;
    }
    
    .teacher-info {
      align-items: center;
      text-align: center;
    }
  }
</style> 