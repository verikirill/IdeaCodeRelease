<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  onMount(() => {
    // Any initialization code can go here
  });
  
  function goToTests() {
    // Will handle navigation to tests
    alert('Переход к тестам');
  }
  
  function goToNotes() {
    // Navigate to the notes page
    goto('/notes');
  }
  
  function goToReminders() {
    // Will handle navigation to reminders
    alert('Переход к напоминаниям');
  }
</script>

<div class="knowledge-page">
  <div class="container">
    <main>
      <div class="header">
        <h1>База знаний</h1>
        <p class="subtitle">Наша цель — ваш результат</p>
      </div>
      
      <div class="knowledge-grid">
        <!-- Тесты минутки -->
        <button class="knowledge-card dark" on:click={goToTests} on:keydown={(e) => e.key === 'Enter' && goToTests()}>
          <h2>Тесты минутки</h2>
          <p class="card-description">
            Физик генерирует небольшие тесты для закрепления материала по пройденной теме
          </p>
          <div class="tests-graphic">
            <img src="/baza.svg" alt="Тесты минутки" class="tests-image" />
          </div>
        </button>
        
        <!-- Готовые конспекты -->
        <button class="knowledge-card orange" on:click={goToNotes} on:keydown={(e) => e.key === 'Enter' && goToNotes()}>
          <h2>Готовые конспекты за два клика</h2>
          <p class="card-description">
            Физик помогает быстро и четко составить конспект для предстоящей пары!
          </p>
          <div class="notes-graphic">
            <img src="/orange.png" alt="Готовые конспекты" class="notes-image" />
          </div>
        </button>
        
        <!-- Напоминания о контрольных -->
        <button class="knowledge-card blue" on:click={goToReminders} on:keydown={(e) => e.key === 'Enter' && goToReminders()}>
          <h2>Напоминания о предстоящих контрольных через телеграм</h2>
          
          <div class="reminder-container">
            <div class="reminder-date">Сегодня</div>
            
            <div class="reminder-card">
              <div class="reminder-subject">Физик</div>
              <div class="reminder-text">
                До итоговой котрольной по дискретной математике осталось 
                2 дня, поспеши подготовиться
              </div>
            </div>
            
            <div class="reminder-card">
              <div class="reminder-subject">Физик</div>
              <div class="reminder-text">
                Я подготовил для вас тесты-минутки по теме основы ООП
              </div>
              <div class="lightning-icon">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="#FFD43B">
                  <path d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
            </div>
            
            <div class="connect-button">
              Подключить напоминания
            </div>
          </div>
        </button>
      </div>
    </main>
  </div>
</div>

<style>
  /* Container */
  .knowledge-page {
    width: 100%;
    min-height: 100vh;
    position: relative;
    padding: 20px 0;
  }
  
  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    box-sizing: border-box;
  }
  
  /* Header */
  .header {
    margin: 40px 0;
    padding-left: calc((100% - 1025px) / 2);
    text-align: left;
  }
  
  h1 {
    font-size: 36px;
    margin: 0 0 10px 0;
    color: #333;
    font-weight: 600;
  }
  
  .subtitle {
    font-size: 18px;
    color: #666;
    margin: 0;
  }
  
  /* Knowledge Grid */
  .knowledge-grid {
    display: grid;
    grid-template-columns: 500px 500px;
    grid-template-rows: auto auto;
    gap: 25px;
    margin-top: 40px;
    justify-content: center;
  }
  
  .knowledge-card {
    border-radius: 20px;
    padding: 30px;
    position: relative;
    overflow: hidden;
    min-height: 250px;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    transition: transform 0.2s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: left;
    border: none;
    font-family: inherit;
  }
  
  .knowledge-card:hover {
    transform: translateY(-5px);
  }
  
  .knowledge-card h2 {
    font-size: 24px;
    margin: 0 0 20px 0;
    font-weight: 600;
    z-index: 2;
    position: relative;
  }
  
  .card-description {
    font-size: 16px;
    line-height: 1.5;
    margin: 0;
    z-index: 2;
    position: relative;
    max-width: 80%;
  }
  
  /* Card varieties */
  .dark {
    background-color: #1E1E1E;
    color: white;
    width: 500px;
    height: 400.47px;
    min-height: unset;
    position: relative;
  }
  
  .dark h2, 
  .dark .card-description {
    position: relative;
    z-index: 2;
    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
  
  .dark .card-description {
    opacity: 0.7;
  }
  
  .orange {
    background-color: #FF6C26;
    color: white;
    position: relative;
    width: 500px;
    height: 500px;
    min-height: unset;
    margin-top: 20%;
  }
  
  .orange h2, 
  .orange .card-description {
    position: relative;
    z-index: 2;
    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
  
  .orange .card-description {
    opacity: 0.7;
  }
  
  .blue {
    background-color: #3B69D5;
    color: white;
    width: 500px;
    min-height: unset;
    height: auto;
    grid-column: 1;
    grid-row: 2;
    margin-top: -40%;
    position: relative;
    overflow: hidden;
  }
  
  .blue h2,
  .blue .reminder-container {
    position: relative;
    z-index: 2;
    text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
  
  /* Add blue background image container */
  .blue::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('/blue.png');
    background-size: cover;
    background-position: center;
    z-index: 1;
  }
  
  /* Notes graphic - updated to fill the entire box */
  .notes-graphic {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 1;
  }
  
  .notes-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 1;
  }
  
  /* Tests graphic - updated with specific image dimensions */
  .tests-graphic {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 1;
  }
  
  .tests-image {
    width: 798px;
    height: 390px;
    object-fit: contain;
    opacity: 1;
    /* Center the image in the container */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  /* Reminder section */
  .reminder-container {
    margin-top: 20px;
    z-index: 2;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: center;
  }
  
  .reminder-date {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 5px;
    text-align: center;
  }
  
  .reminder-card {
    background-color: rgba(0, 0, 0, 0.25);
    border-radius: 15px;
    padding: 15px;
    width: 100%;
    max-width: 420px;
    backdrop-filter: blur(5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .reminder-subject {
    font-weight: 600;
    margin-bottom: 10px;
    color: #4ADE80;
  }
  
  .reminder-text {
    font-size: 14px;
    line-height: 1.5;
    color: white;
  }
  
  .lightning-icon {
    position: absolute;
    bottom: 15px;
    right: 15px;
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .connect-button {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 50px;
    padding: 12px 25px;
    color: white;
    font-size: 16px;
    text-align: center;
    margin-top: 10px;
    width: 90%;
    max-width: 420px;
    cursor: pointer;
    backdrop-filter: blur(5px);
  }
  
  @media (max-width: 1200px) {
    .blue {
      width: 560px;
    }
  }
  
  @media (max-width: 768px) {
    .knowledge-grid {
      justify-content: center;
    }
    
    .dark, .orange, .blue {
      width: 100%;
      max-width: 560px;
    }
    
    .card-description {
      max-width: 100%;
    }
  }
</style> 