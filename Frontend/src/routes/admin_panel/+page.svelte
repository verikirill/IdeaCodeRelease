<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  function navigateToKnowledge() {
    goto('/knowledge');
  }
  
  function navigateToEvents() {
    goto('/afisha');
  }
  
  function navigateToNews() {
    goto('/stories');
  }
  
  onMount(() => {
    // Инициализация при загрузке страницы
  });
</script>

<div class="services-page">
  <div class="container">
    <header>
      <h1>Твой ФФ - университет в одном клике.</h1>
    </header>
    
    <section class="services-section">
      <h2>Сервисы</h2>
      
      <div class="services-grid">
        <div class="service-card" on:click={navigateToKnowledge}>
          <div class="card-icon">
            <img src="/chatbot head.png" alt="База знаний" />
          </div>
          <div class="card-title">База знаний</div>
        </div>
        
        <div class="service-card" on:click={navigateToEvents}>
          <div class="card-icon">
            <img src="/main_page/cute calendar.png" alt="Афиша событий" />
          </div>
          <div class="card-title">Афиша событий</div>
        </div>
        
        <div class="service-card" on:click={navigateToNews}>
          <div class="card-icon">
            <img src="/cute bookmark.png" alt="Новости-сторис" />
          </div>
          <div class="card-title">Новости-сторис</div>
        </div>
      </div>
    </section>
  </div>
</div>

<style>
  .services-page {
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
    text-align: center;
    margin: 40px 0;
  }
  
  h1 {
    font-size: 32px;
    color: #333;
    margin: 0;
    font-weight: 600;
  }
  
  .services-section {
    margin: 40px 0;
  }
  
  h2 {
    font-size: 28px;
    color: #333;
    margin-bottom: 30px;
    font-weight: 500;
    margin-left: 40px;
  }
  
  .services-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: center;
  }
  
  .service-card {
    background-color: #e7e7e7;
    border-radius: 12px;
    width: 300px;
    height: 170px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    padding: 20px;
  }
  
  .service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
  
  .card-icon {
    margin-bottom: 15px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .card-icon img {
    height: 80px;
    width: auto;
    object-fit: contain;
  }
  
  .card-title {
    font-size: 18px;
    font-weight: 500;
    color: #333;
    text-align: center;
  }
  
  @media (max-width: 768px) {
    .services-grid {
      flex-direction: column;
      align-items: center;
    }
    
    .service-card {
      width: 100%;
      max-width: 300px;
    }
  }
</style> 