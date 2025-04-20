<script lang="ts">
  import { onMount } from 'svelte';
  
  let activeSection: string | null = null;
  let showFormModal: boolean = false;
  
  function toggleSection(section: string): void {
    if (activeSection === section) {
      activeSection = null;
    } else {
      activeSection = section;
    }
  }
  
  function openFormModal(): void {
    showFormModal = true;
  }
  
  function closeFormModal(): void {
    showFormModal = false;
  }
  
  onMount(() => {
    // Any initialization code can go here
  });
</script>

<div class="psychologist-background"></div>
<div class="psychologist-page">
  <div class="container">
    <div class="header">
      <h1>Услуги психолога</h1>
      <p class="subtitle">Поддержка психологического здоровья студентов</p>
    </div>
    
    <div class="content">
      <div class="services-grid">
        <div class="service-item" class:active={activeSection === 'individual'} on:click={() => toggleSection('individual')}>
          <div class="service-icon">🧠</div>
          <h3>Индивидуальные консультации</h3>
          <p>Личные встречи с психологом для решения проблем</p>
          
          {#if activeSection === 'individual'}
            <div class="service-details">
              <div class="detail-section">
                <h4>О консультациях</h4>
                <p>Индивидуальные консультации проводятся в комфортной обстановке и полностью конфиденциальны. На встречах вы можете обсудить любые вопросы, которые вас беспокоят.</p>
              </div>
              
              <div class="detail-section">
                <h4>Формат работы</h4>
                <ul>
                  <li>Длительность сессии: 50 минут</li>
                  <li>Периодичность: 1-2 раза в неделю</li>
                  <li>Формат: очно или онлайн</li>
                </ul>
              </div>
              
              <div class="detail-section">
                <h4>Что мы предлагаем</h4>
                <ul>
                  <li>Помощь в преодолении стресса и тревоги</li>
                  <li>Поддержка в период сессии</li>
                  <li>Работа с эмоциональным выгоранием</li>
                  <li>Решение проблем в отношениях</li>
                  <li>Помощь в адаптации к учебе</li>
                </ul>
              </div>
              
              <div class="appointment-block">
                <p>Запись на индивидуальную консультацию открыта для всех студентов факультета</p>
                <button class="secondary-button" on:click={openFormModal}>Записаться</button>
              </div>
            </div>
          {/if}
        </div>
        
        <div class="service-item" class:active={activeSection === 'group'} on:click={() => toggleSection('group')}>
          <div class="service-icon">👥</div>
          <h3>Групповые сессии</h3>
          <p>Терапевтические группы под руководством психолога</p>
          
          {#if activeSection === 'group'}
            <div class="service-details">
              <div class="detail-section">
                <h4>О групповых сессиях</h4>
                <p>Групповые сессии предоставляют уникальную возможность работать над личностными проблемами в поддерживающей среде. Группа становится микромоделью общества, где вы можете безопасно исследовать свои паттерны поведения.</p>
              </div>
              
              <div class="detail-section">
                <h4>Текущие группы</h4>
                <ul>
                  <li><strong>Группа поддержки первокурсников</strong> - каждый вторник 17:00</li>
                  <li><strong>Управление стрессом</strong> - каждый четверг 16:30</li>
                  <li><strong>Развитие коммуникативных навыков</strong> - по субботам 12:00</li>
                </ul>
              </div>
              
              <div class="detail-section">
                <h4>Преимущества группового формата</h4>
                <ul>
                  <li>Разносторонняя обратная связь от участников</li>
                  <li>Возможность увидеть, что вы не одиноки в своих проблемах</li>
                  <li>Развитие навыков межличностного взаимодействия</li>
                  <li>Экономия средств по сравнению с индивидуальными сессиями</li>
                </ul>
              </div>
              
              <div class="appointment-block">
                <p>Для участия в группе необходимо предварительно пройти ознакомительную встречу с психологом</p>
                <button class="secondary-button" on:click={openFormModal}>Записаться на группу</button>
              </div>
            </div>
          {/if}
        </div>
        
        <div class="service-item" class:active={activeSection === 'trainings'} on:click={() => toggleSection('trainings')}>
          <div class="service-icon">📚</div>
          <h3>Психологические тренинги</h3>
          <p>Обучающие программы для развития навыков</p>
          
          {#if activeSection === 'trainings'}
            <div class="service-details">
              <div class="detail-section">
                <h4>О тренингах</h4>
                <p>Наши психологические тренинги — это интенсивные практические занятия для приобретения новых навыков и компетенций. Каждый тренинг включает теоретические блоки и множество упражнений для закрепления материала.</p>
              </div>
              
              <div class="detail-section">
                <h4>Расписание тренингов</h4>
                <ul>
                  <li><strong>Эмоциональный интеллект</strong> - 15-16 ноября</li>
                  <li><strong>Эффективное целеполагание</strong> - 25 ноября</li>
                  <li><strong>Уверенное поведение и ассертивность</strong> - 5-6 декабря</li>
                  <li><strong>Практики осознанности (mindfulness)</strong> - 18 декабря</li>
                </ul>
              </div>
              
              <div class="detail-section">
                <h4>Что вы получите</h4>
                <ul>
                  <li>Практические инструменты для повседневного применения</li>
                  <li>Методические материалы и рабочие тетради</li>
                  <li>Сертификат о прохождении тренинга</li>
                  <li>Возможность задать вопросы эксперту</li>
                </ul>
              </div>
              
              <div class="appointment-block">
                <p>Количество мест ограничено, требуется предварительная регистрация</p>
                <button class="secondary-button" on:click={openFormModal}>Забронировать место</button>
              </div>
            </div>
          {/if}
        </div>
        
        <div class="service-item" class:active={activeSection === 'development'} on:click={() => toggleSection('development')}>
          <div class="service-icon">🌱</div>
          <h3>Программы саморазвития</h3>
          <p>Курсы для личностного роста и самопознания</p>
          
          {#if activeSection === 'development'}
            <div class="service-details">
              <div class="detail-section">
                <h4>О программах саморазвития</h4>
                <p>Долгосрочные программы саморазвития разработаны для всестороннего личностного роста. Они сочетают в себе индивидуальную работу, групповые занятия и самостоятельную практику под руководством опытных психологов.</p>
              </div>
              
              <div class="detail-section">
                <h4>Текущие программы</h4>
                <ul>
                  <li><strong>"Путь к себе"</strong> - 3-месячная программа самопознания и развития самосознания</li>
                  <li><strong>"Гармония отношений"</strong> - 2-месячный курс по улучшению межличностных отношений</li>
                  <li><strong>"Стрессоустойчивость"</strong> - 6-недельная программа развития устойчивости к стрессу</li>
                </ul>
              </div>
              
              <div class="detail-section">
                <h4>Структура программ</h4>
                <ul>
                  <li>Диагностический этап (определение точки отсчета)</li>
                  <li>Еженедельные групповые занятия</li>
                  <li>Индивидуальные консультации с куратором</li>
                  <li>Дневник саморефлексии и домашние задания</li>
                  <li>Завершающая диагностика и планирование дальнейшего развития</li>
                </ul>
              </div>
              
              <div class="appointment-block">
                <p>Для участия необходимо пройти предварительное собеседование с руководителем программы</p>
                <button class="secondary-button" on:click={openFormModal}>Подать заявку</button>
              </div>
            </div>
          {/if}
        </div>
      </div>
      
      <div class="contact-section">
        <h2>Как связаться с психологической службой</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <div class="contact-icon">📞</div>
            <h3>Телефон</h3>
            <p>+7 (800) 123-45-67</p>
            <p class="contact-note">Пн-Пт: 9:00 - 18:00</p>
          </div>
          
          <div class="contact-item">
            <div class="contact-icon">📱</div>
            <h3>Телеграм</h3>
            <p>@ff_psychology</p>
            <p class="contact-note">Быстрый способ связи</p>
          </div>
          
          <div class="contact-item">
            <div class="contact-icon">📧</div>
            <h3>Email</h3>
            <p>psychology@ff.edu</p>
            <p class="contact-note">Ответ в течение 24 часов</p>
          </div>
          
          <div class="contact-item">
            <div class="contact-icon">🏢</div>
            <h3>Кабинет</h3>
            <p>Корпус А, каб. 305</p>
            <p class="contact-note">Часы приема: 10:00 - 17:00</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

{#if showFormModal}
  <div class="modal-overlay" on:click={closeFormModal}>
    <div class="modal-container" on:click|stopPropagation>
      <button class="close-modal" on:click={closeFormModal}>×</button>
      <div class="modal-content">
        <h2>Запись на консультацию к психологу</h2>
        <div class="google-form-container">
          <iframe 
            src="https://docs.google.com/forms/d/e/1FAIpQLSf2tHo2jLKfA1V_WTjQD1Qc8tzylXVtpreGZHGy2yS_itWj1w/viewform?embedded=true" 
            width="100%" 
            height="600" 
            frameborder="0" 
            marginheight="0" 
            marginwidth="0">
            Загрузка...
          </iframe>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .psychologist-background {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100vh;
    background-image: url('/glavnaya_grad.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    z-index: -10;
    pointer-events: none;
  }

  .psychologist-page {
    width: 100%;
    min-height: 100vh;
    padding: 20px 0;
    position: relative;
    z-index: 1;
    pointer-events: auto;
  }
  
  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    box-sizing: border-box;
    background-color: transparent;
  }
  
  .header {
    margin: 40px 0;
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
    line-height: 1.4;
  }
  
  .content {
    display: flex;
    flex-direction: column;
    gap: 40px;
  }
  
  .services-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
  }
  
  .service-item {
    background-color: #ffffff;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  
  .service-item:hover {
    transform: translateY(-5px);
  }
  
  .service-item.active {
    grid-column: span 2;
  }
  
  .service-icon {
    font-size: 40px;
    margin-bottom: 15px;
  }
  
  .service-item h3 {
    margin: 0 0 10px 0;
    font-size: 20px;
    color: #333;
  }
  
  .service-item p {
    margin: 0;
    font-size: 16px;
    color: #666;
    line-height: 1.5;
  }
  
  .service-details {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    animation: fadeIn 0.3s ease;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  .detail-section {
    margin-bottom: 20px;
  }
  
  .detail-section h4 {
    font-size: 18px;
    margin: 0 0 10px 0;
    color: #333;
  }
  
  .detail-section ul {
    margin: 0;
    padding-left: 20px;
  }
  
  .detail-section li {
    margin-bottom: 8px;
    color: #555;
  }
  
  .appointment-block {
    background-color: #e8f0ff;
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
  }
  
  .appointment-block p {
    margin: 5px 0;
    flex: 1;
    min-width: 200px;
  }
  
  .secondary-button {
    background-color: #8A2BE2;
    color: white;
    border: none;
    border-radius: 30px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .secondary-button:hover {
    background-color: #7B1FA2;
  }
  
  .contact-section {
    margin-top: 20px;
  }
  
  .contact-section h2 {
    margin-bottom: 20px;
    font-size: 24px;
    color: #333;
  }
  
  .contact-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
  
  .contact-item {
    background-color: #ffffff;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  }
  
  .contact-icon {
    font-size: 30px;
    margin-bottom: 10px;
  }
  
  .contact-item h3 {
    margin: 0 0 10px 0;
    font-size: 18px;
    color: #333;
  }
  
  .contact-item p {
    margin: 0;
    font-size: 16px;
    color: #666;
  }
  
  .contact-note {
    font-size: 14px !important;
    color: #888 !important;
    margin-top: 5px !important;
  }
  
  /* Modal styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
  }
  
  .modal-container {
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    background-color: white;
    border-radius: 20px;
    position: relative;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  
  .close-modal {
    position: absolute;
    top: 15px;
    right: 20px;
    background: none;
    border: none;
    font-size: 28px;
    color: #333;
    cursor: pointer;
    z-index: 10;
  }
  
  .modal-content {
    padding: 30px;
    overflow-y: auto;
  }
  
  .modal-content h2 {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 24px;
    color: #333;
  }
  
  .google-form-container {
    height: 600px;
    overflow: hidden;
  }
  
  .google-form-container iframe {
    border: none;
  }
  
  @media (max-width: 992px) {
    .contact-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (max-width: 768px) {
    .services-grid {
      grid-template-columns: 1fr;
    }
    
    .service-item.active {
      grid-column: span 1;
    }
    
    .appointment-block {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .appointment-block button {
      margin-top: 10px;
      align-self: flex-start;
    }
    
    .modal-container {
      max-height: 80vh;
    }
  }
  
  @media (max-width: 576px) {
    .contact-grid {
      grid-template-columns: 1fr;
    }
    
    .modal-content {
      padding: 20px 15px;
    }
    
    .google-form-container {
      height: 500px;
    }
  }
</style> 