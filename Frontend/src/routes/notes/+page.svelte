<script lang="ts">
  import { onMount } from 'svelte';
  
  interface Message {
    sender: 'user' | 'bot';
    text: string;
    isLink?: boolean;
  }
  
  let messages: Message[] = [
    {
      sender: 'bot',
      text: 'Напиши мне название темы, по которой я составлю конспект, дополнительно можно указать размер и ключевое'
    }
  ];
  
  let userMessage = '';
  let chatContainer: HTMLElement;
  let currentDate = new Date();
  let formattedDate = `${currentDate.getDate()} ${getMonthName(currentDate.getMonth())}`;
  let botAvatar = '/chatbot head.png';
  let isProcessing = false;
  let demoLinks = [
    'https://ffhack',
    'https://diskretka'
  ];
  
  function getMonthName(monthIndex: number): string {
    const months = [
      'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
      'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ];
    return months[monthIndex];
  }
  
  function sendMessage() {
    if (!userMessage.trim() || isProcessing) return;
    
    // Add user message
    messages = [...messages, { sender: 'user', text: userMessage }];
    const sentMessage = userMessage;
    userMessage = '';
    isProcessing = true;
    
    // Simulate bot response after a delay
    setTimeout(() => {
      // First response - echoing the topic
      messages = [...messages, { 
        sender: 'bot', 
        text: `Интегралы. Несобственные интегралы.` 
      }];
      
      // Simulate processing delay
      setTimeout(() => {
        // Final response with link
        messages = [...messages, { 
          sender: 'bot', 
          text: `Готово! Посмотреть можно по ссылке\nhttps://ffhack`
        }];
        isProcessing = false;
        
        // Scroll to bottom
        setTimeout(() => {
          if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
          }
        }, 100);
      }, 1500);
    }, 1000);
  }
  
  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }
  
  onMount(() => {
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  });
</script>

<div class="notes-page">
  <div class="container">
    <div class="header">
      <h1>Конспекты</h1>
      <p class="subtitle">Самое основное на лекции<br>в два клика</p>
    </div>
    
    <div class="content-layout">
      <div class="chat-container" bind:this={chatContainer}>
        <div class="chat-header">
          <div class="bot-info">
            <img src={botAvatar} alt="Физик чат-бот" class="bot-avatar">
            <span class="bot-name">Физик чат-бот</span>
            <span class="bot-settings">⚙️</span>
          </div>
          <div class="chat-date">{formattedDate}</div>
        </div>
        
        <div class="messages">
          {#each messages as message}
            <div class="message {message.sender}">
              {#if message.sender === 'bot'}
                <div class="avatar-container">
                  <img src={botAvatar} alt="Физик" class="avatar">
                </div>
              {/if}
              
              <div class="message-content">
                {#if message.sender === 'bot' && message.text.includes('Готово!')}
                  <div class="sender-name">Физик</div>
                  <div class="message-text">
                    Готово! Посмотреть можно по ссылке
                    <a href="https://ffhack" class="message-link">https://ffhack</a>
                  </div>
                {:else}
                  {#if message.sender === 'bot'}
                    <div class="sender-name">Физик</div>
                  {/if}
                  <div class="message-text">{message.text}</div>
                {/if}
              </div>
            </div>
          {/each}
          
          {#if isProcessing}
            <div class="message bot">
              <div class="avatar-container">
                <img src={botAvatar} alt="Физик" class="avatar">
              </div>
              <div class="message-content">
                <div class="sender-name">Физик</div>
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          {/if}
        </div>
        
        <div class="message-input">
          <input
            type="text"
            placeholder="Ваше сообщение"
            bind:value={userMessage}
            on:keydown={handleKeyPress}
            disabled={isProcessing}
          >
          <button class="send-button" on:click={sendMessage} disabled={isProcessing}>
            <span>➤</span>
          </button>
        </div>
      </div>
      
      <div class="sidebar">
        <div class="sidebar-section">
          <h2 class="sidebar-title">
            <span class="sidebar-icon">≡</span> Ссылка на конспект
          </h2>
          <div class="link-item">
            <span class="link-icon">📄</span>
            <a href="https://ffhack" class="sidebar-link">https://ffhack</a>
          </div>
        </div>
        
        <div class="sidebar-section">
          <h2 class="sidebar-title">
            <span class="sidebar-icon">≡</span> Последние конспекты
          </h2>
          {#each demoLinks as link}
            <div class="link-item">
              <span class="link-icon">📄</span>
              <a href={link} class="sidebar-link">{link}</a>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .notes-page {
    width: 100%;
    min-height: 100vh;
    padding: 20px 0;
  }
  
  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    box-sizing: border-box;
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
  
  .content-layout {
    display: flex;
    gap: 25px;
    margin-top: 40px;
  }
  
  .chat-container {
    flex: 1;
    background-color: #f5f5f5;
    border-radius: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 650px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
  
  .chat-header {
    padding: 15px 20px;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .bot-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .bot-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .bot-name {
    font-weight: 500;
    font-size: 16px;
  }
  
  .bot-settings {
    cursor: pointer;
    opacity: 0.7;
    font-size: 18px;
  }
  
  .chat-date {
    color: #888;
    font-size: 14px;
  }
  
  .messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .message {
    display: flex;
    gap: 10px;
    max-width: 80%;
  }
  
  .message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
  }
  
  .message.bot {
    align-self: flex-start;
  }
  
  .avatar-container {
    width: 36px;
    height: 36px;
    flex-shrink: 0;
  }
  
  .avatar {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .message-content {
    background-color: white;
    padding: 12px 15px;
    border-radius: 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .message.user .message-content {
    background-color: #2b5cda;
    color: white;
  }
  
  .sender-name {
    font-weight: 500;
    margin-bottom: 5px;
    font-size: 14px;
    color: #555;
  }
  
  .message.user .sender-name {
    display: none;
  }
  
  .message-text {
    line-height: 1.4;
    white-space: pre-line;
  }
  
  .message-link {
    color: #2b5cda;
    text-decoration: underline;
  }
  
  .message.user .message-link {
    color: white;
  }
  
  .typing-indicator {
    display: flex;
    gap: 3px;
    padding: 5px 0;
  }
  
  .typing-indicator span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #aaa;
    animation: typing 1.4s infinite ease-in-out;
  }
  
  .typing-indicator span:nth-child(1) {
    animation-delay: 0s;
  }
  
  .typing-indicator span:nth-child(2) {
    animation-delay: 0.2s;
  }
  
  .typing-indicator span:nth-child(3) {
    animation-delay: 0.4s;
  }
  
  @keyframes typing {
    0%, 60%, 100% {
      transform: translateY(0);
      opacity: 0.6;
    }
    30% {
      transform: translateY(-5px);
      opacity: 1;
    }
  }
  
  .message-input {
    padding: 15px;
    border-top: 1px solid #e0e0e0;
    display: flex;
    gap: 10px;
  }
  
  .message-input input {
    flex: 1;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    font-size: 15px;
    outline: none;
  }
  
  .message-input input:focus {
    border-color: #2b5cda;
  }
  
  .send-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #2b5cda;
    border: none;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .send-button:hover {
    background-color: #1a4cba;
  }
  
  .send-button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
  }
  
  .sidebar {
    width: 320px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 25px;
  }
  
  .sidebar-section {
    background-color: #f5f5f5;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
  
  .sidebar-title {
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 15px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .sidebar-icon {
    color: #666;
  }
  
  .link-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }
  
  .link-icon {
    color: #666;
  }
  
  .sidebar-link {
    color: #2b5cda;
    text-decoration: none;
  }
  
  .sidebar-link:hover {
    text-decoration: underline;
  }
  
  @media (max-width: 992px) {
    .content-layout {
      flex-direction: column;
    }
    
    .sidebar {
      width: 100%;
    }
  }
  
  @media (max-width: 768px) {
    .message {
      max-width: 90%;
    }
  }
</style> 