<script lang="ts">
  import ChatBot from '$lib/components/ChatBot.svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import Profile from '$lib/components/Profile.svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { authStore } from '$lib/services/auth';
  import { browser } from '$app/environment';
  
  $: isAuthPage = $page.url.pathname === '/login' || $page.url.pathname === '/register';
  $: isAdminPanelPage = $page.url.pathname === '/admin_panel';

  onMount(async () => {
    if (browser) {
      // Проверяем, есть ли сохраненный токен
      const savedToken = localStorage.getItem('access_token');
      if (savedToken) {
        // Если токен существует, попробуем восстановить данные пользователя
        await authStore.fetchUserData();
      }
    }
  });
</script>

<div class="app">
  {#if !isAuthPage}
    <Navbar />
    <Profile />
  {/if}

  <main>
    <slot></slot>
  </main>
</div>

<style>
  /* Глобальные стили */
  :global(html) {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
  }

  :global(body) {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    min-height: 100vh;
    position: relative;
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #ffffff;
    /* Обеспечиваем корректное отображение на мобильных устройствах */
    -webkit-text-size-adjust: 100%;
  }
  
  /* Определение шрифтов */
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

  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .top-header {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding: 15px 0;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
  }

  .nav-buttons {
    display: flex;
    gap: 15px;
    margin: 0 auto;
  }

  .nav-button {
    display: flex;
    align-items: center;
    padding: 8px 15px;
    border-radius: 8px;
    background-color: #fff;
    color: #333;
    text-decoration: none;
    font-weight: 500;
    border: 1px solid #e0e0e0;
    transition: all 0.2s ease;
  }

  .nav-button.active {
    background-color: #1A3882;
    color: white;
    border-color: #1A3882;
  }

  .nav-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .icon {
    margin-left: 8px;
  }

  .profile-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    text-decoration: none;
    border: 1px solid #e0e0e0;
  }

  main {
    flex: 1;
  }

  @media (max-width: 768px) {
    .app-container {
      padding: 0;
    }
  }
</style> 