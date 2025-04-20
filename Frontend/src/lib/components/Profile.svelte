<script>
  import { authStore } from '$lib/services/auth';
  import { onMount } from 'svelte';
  
  export let avatar = '/avatar.png';
  let isMenuOpen = false;
  let user = null;
  let isAuthenticated = false;
  const API_URL = 'http://localhost:8000'; // Базовый URL API
  
  onMount(() => {
    // Подписываемся на изменения в хранилище пользователя
    const unsubUserData = authStore.user.subscribe(value => {
      user = value;
      if (user && user.avatar) {
        // Проверяем, начинается ли путь с http или /
        if (user.avatar.startsWith('http')) {
          avatar = user.avatar;
        } else {
          // Если путь относительный, добавляем базовый URL API
          avatar = `${API_URL}${user.avatar}`;
        }
      }
    });
    
    // Подписываемся на статус аутентификации
    const unsubAuth = authStore.isAuthenticated.subscribe(value => {
      isAuthenticated = value;
    });
    
    return () => {
      unsubUserData();
      unsubAuth();
    };
  });
  
  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }
  
  function handleLogout() {
    authStore.logout();
    isMenuOpen = false;
  }
</script>

<div class="profile">
  <div class="avatar" on:click={toggleMenu}>
    {#if isAuthenticated}
      <img src={avatar} alt="Профиль" />
    {:else}
      <img src="/avatar_placeholder.png" alt="Гость" />
    {/if}
  </div>
  
  {#if isMenuOpen}
    <div class="menu">
      {#if isAuthenticated && user}
        <div class="user-info">
          <span class="username">{user.first_name} {user.last_name}</span>
          <span class="email">{user.email}</span>
        </div>
        <ul>
          <li><a href="/account" class="profile-link">Мой профиль</a></li>
          <li><button on:click={handleLogout}>Выйти</button></li>
        </ul>
      {:else}
        <ul class="auth-options">
          <li><a href="/login" class="auth-link">Вход</a></li>
          <li><a href="/register" class="auth-link">Регистрация</a></li>
        </ul>
      {/if}
    </div>
  {/if}
</div>

<style>
  .profile {
    position: fixed;
    top: 15px;
    right: 40px;
    z-index: 100;
  }

  .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #f3f3f3;
    cursor: pointer;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .avatar:hover {
    transform: scale(1.05);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
  }
  
  .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .menu {
    position: absolute;
    top: 60px;
    right: 0;
    width: 220px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    padding: 10px 0;
    z-index: 101;
    animation: fadeIn 0.2s ease-out;
    overflow: hidden;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .user-info {
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
  }
  
  .username {
    display: block;
    font-weight: 500;
    font-size: 15px;
    margin-bottom: 4px;
  }
  
  .email {
    display: block;
    font-size: 13px;
    color: #666;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    width: 100%;
  }
  
  li {
    padding: 0;
    width: 100%;
  }
  
  li a, li button {
    display: block;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    font-size: 14px;
    text-align: left;
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s;
    box-sizing: border-box;
  }
  
  li a:hover, li button:hover {
    background-color: #f5f5f5;
  }
  
  .profile-link {
    color: #333;
  }
  
  li button {
    color: #d32f2f;
    font-weight: 500;
  }
  
  .auth-options {
    padding: 5px 0;
    width: 100%;
  }
  
  .auth-link {
    font-weight: 500;
    color: #1A3882;
    transition: background-color 0.2s;
  }
  
  .auth-link:hover {
    background-color: #f0f7ff;
  }
</style>