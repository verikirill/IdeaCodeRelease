<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import { authStore } from '$lib/services/auth';
  import { goto } from '$app/navigation';
  
  let avatar = '/avatar.png';
  let showStories = false;
  let currentStoryIndex = 0;
  let prevStoryIndex = 0;
  let direction = 1; // 1 для вперед, -1 для назад
  let cardsReady = false; // Flag to control the animation of service cards
  
  interface Story {
    id: number;
    image: string;
    title: string;
    content: string;
  }
  
  let stories: Story[] = [
    {
      id: 1,
      image: '/main_page/stories1.png',
      title: 'Новости факультета',
      content: 'Подробное содержание новостей факультета. Здесь будет отображаться полная информация о событии.'
    },
    {
      id: 2,
      image: '/main_page/stories2.png',
      title: 'Студенческая жизнь',
      content: 'Подробное содержание о студенческой жизни. Здесь будет отображаться полная информация о событии.'
    },
    {
      id: 3,
      image: '/main_page/stories3.png',
      title: 'Научные достижения',
      content: 'Подробное содержание о научных достижениях. Здесь будет отображаться полная информация о событии.'
    },
    {
      id: 4,
      image: '/main_page/stories4.png',
      title: 'Конференции',
      content: 'Подробное содержание о конференциях. Здесь будет отображаться полная информация о событии.'
    },
    {
      id: 5,
      image: '/main_page/stories5.png',
      title: 'Стажировки',
      content: 'Подробное содержание о стажировках. Здесь будет отображаться полная информация о событии.'
    },
    {
      id: 6,
      image: '/main_page/stories6.png',
      title: 'Спортивные события',
      content: 'Подробное содержание о спортивных событиях. Здесь будет отображаться полная информация о событии.'
    }
  ];
  
  // Услуги на главной странице
  interface Service {
    title: string;
    image: string;
    link?: string;
  }
  
  let services: Service[] = [
    {
      title: 'Карта\nкорпусов',
      image: '/main_page/map and pencil.png',
      link: 'https://app.profcomff.com/apps/2'
    },
    {
      title: 'Афиша\nмероприятий',
      image: '/main_page/cute calendar.png',
      link: '/afisha'
    },
    {
      title: 'База\nзнаний',
      image: '/main_page/cute books.png',
      link: '/knowledge'
    },
    {
      title: 'Бюро\nнаходок',
      image: '/main_page/search cute blue icon.png'
    },
    {
      title: 'Меню\nстоловой',
      image: '/main_page/cute shopping basket.png',
      link: '/menu'
    },
    {
      title: 'Мемы\nот студентов',
      image: '/main_page/emoji with tongue.png'
    },
    {
      title: 'Отзывы\nо преподавателях',
      image: '/main_page/cute smiling star.png',
      link: '/reviews'
    },
    {
      title: 'Пропуск\nна машину',
      image: '/main_page/document file with code symbol.png'
    },
    {
      title: 'Калькулятор\nстипендий',
      image: '/main_page/banknotes.png'
    },
    {
      title: 'Бесплатный\nпринтер',
      image: '/main_page/cash receipt.png'
    },
    {
      title: 'Вступить\nв профком',
      image: '/main_page/two speech bubbles.png'
    }
  ];
  
  function openStories(index: number) {
    currentStoryIndex = index;
    prevStoryIndex = index;
    showStories = true;
  }
  
  function closeStories() {
    showStories = false;
  }
  
  function nextStory() {
    if (currentStoryIndex < stories.length - 1) {
      prevStoryIndex = currentStoryIndex;
      direction = 1;
      currentStoryIndex++;
    } else {
      closeStories();
    }
  }
  
  function prevStory() {
    if (currentStoryIndex > 0) {
      prevStoryIndex = currentStoryIndex;
      direction = -1;
      currentStoryIndex--;
    }
  }
  
  // Функция обновления аватара на основе авторизации
  function updateAvatar() {
    // Использовать isAuthenticated из authStore
    if (!authStore.isAuthenticated) {
      avatar = '/static/main_page/icon_profile.svg';
    }
  }
  
  // Функция для программной навигации
  function navigateTo(url: string) {
    if (url.startsWith('http')) {
      // Для внешних ссылок открываем в новой вкладке
      window.open(url, '_blank');
    } else {
      // Для внутренних используем goto
      goto(url);
    }
  }
  
  onMount(() => {
    // Обновить аватар при загрузке страницы
    updateAvatar();
    
    // Подписаться на изменения в authStore
    const unsubscribe = authStore.isAuthenticated.subscribe(value => {
      if (!value) {
        avatar = '/static/main_page/icon_profile.svg';
      } else {
        avatar = '/avatar.png';
      }
    });

    // Trigger animation for service cards after a short delay
    setTimeout(() => {
      cardsReady = true;
    }, 500);
    
    return () => {
      // Отписаться при уничтожении компонента
      unsubscribe();
    };
  });
</script>

<div class="main-page"></div>
<div class="main-content">
  <div class="container">
    <main>
      <h1 class="main-title">Твой ФФ - университет в одном клике.</h1>

      <!-- Main circular buttons -->
      <div class="circular-buttons">
        {#each stories as story, index}
          <div class="circular-button" on:click={() => openStories(index)}>
            <img src={story.image} alt={story.title} class="story-image">
          </div>
        {/each}
      </div>

      <!-- Services section -->
      <section class="services">
        <h2>Сервисы</h2>
        <div class="services-grid">
          {#each services as service, i}
            {#if cardsReady}
              <div class="service-card" 
                   in:fly={{ y: 50, duration: 400, delay: i * 100, easing: cubicOut }} 
                   on:click={() => service.link && navigateTo(service.link)} 
                   class:clickable={service.link}>
                <h3>{service.title}</h3>
                <div class="service-icon">
                  <img src={service.image} alt={service.title} />
                </div>
              </div>
            {:else}
              <div class="service-card service-card-hidden"
                   class:clickable={service.link}>
                <h3>{service.title}</h3>
                <div class="service-icon">
                  <img src={service.image} alt={service.title} />
                </div>
              </div>
            {/if}
          {/each}
        </div>
      </section>
    </main>
  </div>

  {#if showStories}
    <div class="stories-overlay" transition:fade={{ duration: 200 }}>
      <div class="stories-slider">
        <div class="progress-bar">
          {#each stories as _, i}
            <div class="progress-segment {i === currentStoryIndex ? 'active' : i < currentStoryIndex ? 'completed' : ''}"></div>
          {/each}
        </div>
        
        <button class="close-stories" on:click={closeStories}>&times;</button>

        <div class="stories-carousel">
          {#if currentStoryIndex > 1}
            <div class="story-card far-prev-card" 
                on:click={() => prevStory()}>
              <div class="card-content">
                <div class="story-image-container">
                  <img src={"/main_page/stories (" + (currentStoryIndex - 1) + ").png"} alt={stories[currentStoryIndex - 2].title} />
                </div>
              </div>
              <div class="card-overlay"></div>
            </div>
          {/if}

          {#if currentStoryIndex > 0}
            <div class="story-card prev-card" 
                on:click={() => prevStory()}>
              <div class="card-content">
                <div class="story-image-container">
                  <img src={"/main_page/stories (" + currentStoryIndex + ").png"} alt={stories[currentStoryIndex - 1].title} />
                </div>
              </div>
              <div class="card-overlay"></div>
            </div>
          {/if}
          
          <div class="story-card current-card">
            {#key currentStoryIndex}
            <div class="story-image-container"
                in:fade={{ duration: 550, easing: cubicOut }}>
              <img src={"/main_page/stories (" + (currentStoryIndex + 1) + ").png"} alt={stories[currentStoryIndex].title} />
            </div>
            {/key}
          </div>
          
          {#if currentStoryIndex < stories.length - 1}
            <div class="story-card next-card"
                on:click={() => nextStory()}>
              <div class="card-content">
                <div class="story-image-container">
                  <img src={"/main_page/stories (" + (currentStoryIndex + 2) + ").png"} alt={stories[currentStoryIndex + 1].title} />
                </div>
              </div>
              <div class="card-overlay"></div>
            </div>
          {/if}

          {#if currentStoryIndex < stories.length - 2}
            <div class="story-card far-next-card"
                on:click={() => nextStory()}>
              <div class="card-content">
                <div class="story-image-container">
                  <img src={"/main_page/stories (" + (currentStoryIndex + 3) + ").png"} alt={stories[currentStoryIndex + 2].title} />
                </div>
              </div>
              <div class="card-overlay"></div>
            </div>
          {/if}
        </div>
        
        <div class="story-navigation">
          <button class="story-nav-button prev" on:click={prevStory} disabled={currentStoryIndex === 0}>
            <span>❮</span>
          </button>
          <button class="story-nav-button next" on:click={nextStory} disabled={currentStoryIndex === stories.length - 1}>
            <span>❯</span>
          </button>
        </div>
      </div>
    </div>
  {/if}
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

  /* Фон страницы */
  .main-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('/main_page/main_background.png');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    z-index: -1;
  }
  
  .main-content {
    position: relative;
    min-height: 100vh;
    z-index: 1;
  }

  /* Container */
  .container {
    padding: 0;
    width: 100%;
    margin: 0 auto;
    position: relative;
    overflow-x: hidden;
  }
  
  /* Main content */
  main {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    box-sizing: border-box;
    width: 100%;
  }

  .main-title {
    text-align: center;
    margin: 20px 0;
    font-size: 28px;
  }

  /* Circular buttons */
  .circular-buttons {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 15px;
    margin: 20px auto;
    width: 100%;
    padding: 0;
  }

  .circular-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 10px;
    cursor: pointer;
  }

  .story-image {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: cover;
  }

  /* Services section */
  .services {
    margin: 40px auto;
    padding: 0;
    width: 100%;
    text-align: left;
  }

  .services h2 {
    margin-bottom: 25px;
    font-size: 32px;
    text-align: left;
    padding-left: 35px;
    font-weight: 600;
  }

  .services-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    width: 95%;
    margin: 0 auto;
    padding: 0 20px;
  }

  .service-card {
    background-color: #F2F2F2;
    border-radius: 18px;
    padding: 18px 25px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    aspect-ratio: 2.4 / 1;
    transition: transform 0.2s ease;
    position: relative;
    text-align: left;
    margin: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    overflow: hidden;
  }
  
  .service-card-hidden {
    opacity: 0;
  }
  
  .service-card.clickable {
    cursor: pointer;
  }

  .service-card:hover {
    transform: translateY(-3px);
  }

  .service-card h3 {
    margin: 0;
    font-size: 22px;
    font-weight: 600;
    line-height: 1.2;
    text-align: left;
    width: 60%;
    white-space: pre-wrap;
    position: relative;
    z-index: 2;
  }

  .service-icon {
    position: absolute;
    bottom: 12px;
    right: 25px;
    width: 25%;
    height: 75%;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    z-index: 1;
  }

  .service-icon img {
    width: 100%;
    height: auto;
    object-fit: contain;
    max-height: 100%;
  }

  .card-link {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    text-decoration: none;
    color: inherit;
    justify-content: flex-start;
    align-items: flex-start;
    position: relative;
  }

  /* Stories Overlay */
  .stories-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.9);
    z-index: 2000;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
  }
  
  .stories-slider {
    position: relative;
    width: 100%;
    max-width: 1200px;
    height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 50px;
  }
  
  .progress-bar {
    display: flex;
    gap: 5px;
    width: 400px;
    margin-bottom: 15px;
    z-index: 20;
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .progress-segment {
    height: 3px;
    flex: 1;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
    transition: background-color 0.3s ease;
  }
  
  .progress-segment.active {
    background-color: #1A3882;
    animation: progress 5s linear;
  }
  
  @keyframes progress {
    from { background-color: #1A3882; width: 0; }
    to { background-color: #1A3882; width: 100%; }
  }
  
  .close-stories {
    position: absolute;
    top: 10px;
    right: 20px;
    background: none;
    border: none;
    font-size: 30px;
    color: white;
    cursor: pointer;
    z-index: 10;
  }
  
  .stories-carousel {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 80vh;
    position: relative;
  }
  
  .story-card {
    position: relative;
    border-radius: 40px;
    overflow: hidden;
    transition: all 0.3s ease;
    background-color: #E4E4E4;
    flex-shrink: 0;
    aspect-ratio: 9/16;
  }
  
  .current-card {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 350px;
    z-index: 5;
    padding: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  .prev-card {
    position: absolute;
    left: calc(50% - 470px);
    top: 50%;
    transform: translateY(-50%);
    width: 250px;
    z-index: 3;
    cursor: pointer;
    transition: opacity 0.5s ease;
  }
  
  .next-card {
    position: absolute;
    left: calc(50% + 220px);
    top: 50%;
    transform: translateY(-50%);
    width: 250px;
    z-index: 3;
    cursor: pointer;
    transition: opacity 0.5s ease;
  }
  
  .far-prev-card {
    position: absolute;
    left: calc(50% - 690px);
    top: 50%;
    transform: translateY(-50%);
    width: 200px;
    z-index: 1;
    cursor: pointer;
    transition: opacity 0.5s ease;
  }
  
  .far-next-card {
    position: absolute;
    left: calc(50% + 490px);
    top: 50%;
    transform: translateY(-50%);
    width: 200px;
    z-index: 1;
    cursor: pointer;
    transition: opacity 0.5s ease;
  }
  
  .prev-card:hover, .next-card:hover {
    transform: translateY(-50%);
  }
  
  .far-prev-card:hover, .far-next-card:hover {
    transform: translateY(-50%);
  }
  
  .card-content {
    padding: 0;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    position: relative;
    z-index: 1;
  }
  
  .card-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 2;
  }
  
  .far-prev-card .card-overlay, 
  .far-next-card .card-overlay {
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .story-title {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }
  
  .story-image-container {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
    border-radius: 40px;
    overflow: hidden;
  }
  
  .story-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .story-description {
    font-size: 16px;
    line-height: 1.5;
    color: #333;
    flex-grow: 1;
    overflow-y: auto;
  }
  
  .prev-card .story-description, 
  .next-card .story-description {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }
  
  /* Story Navigation */
  .story-navigation {
    position: fixed;
    top: 50%;
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 0;
    transform: translateY(-50%);
    pointer-events: none;
    z-index: 10;
    left: 0;
    right: 0;
  }
  
  .story-nav-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.2);
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
    color: white;
    cursor: pointer;
    pointer-events: auto;
    margin: 0 20px;
  }
  
  .story-nav-button.prev {
    margin-left: 30px;
  }
  
  .story-nav-button.next {
    margin-right: 30px;
  }
  
  .story-nav-button:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  @media (max-width: 768px) {
    .services-grid {
      grid-template-columns: 1fr;
      padding: 0 20px;
    }
    
    .services h2 {
      padding-left: 25px;
      font-size: 28px;
    }
    
    .service-card {
      padding: 16px 20px;
      aspect-ratio: 2.6 / 1;
    }
    
    .service-card h3 {
      font-size: 20px;
      width: 65%;
    }
    
    .service-icon {
      bottom: 10px;
      right: 20px;
      height: 70%;
    }
    
    .circular-buttons {
      gap: 10px;
    }
    
    .circular-button {
      margin: 0 5px;
    }
    
    .story-image {
      width: 70px;
      height: 70px;
    }
  }
</style>
