<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/services/auth';
  import { searchGroups, getUserGroup, selectUserGroup } from '$lib/services/timetable';
  import { goto } from '$app/navigation';
  import type { UserData } from '$lib/services/auth';
  import type { Group } from '$lib/services/timetable';
  
  let user: UserData | null = null;
  let isLoading = true;
  let selectedGroup: Group | null = null;
  let isLoadingGroup = true;
  let searchQuery = '';
  let searchResults: Group[] = [];
  let showDropdown = false;
  let isChangingGroup = false;
  let changeSuccessful = false;
  
  // Редактирование профиля
  let isEditMode = false;
  let editData = {
    first_name: '',
    last_name: '',
    bio: '',
    phone: ''
  };
  let isSaving = false;
  let saveSuccess = false;
  let saveError = '';
  
  onMount(async () => {
    const unsubAuth = authStore.isAuthenticated.subscribe((isAuth) => {
      if (!isAuth) {
        goto('/login');
      }
    });
    
    const unsubUser = authStore.user.subscribe((userData) => {
      user = userData;
      isLoading = false;
      
      // Инициализируем данные для редактирования
      if (user) {
        editData = {
          first_name: user.first_name || '',
          last_name: user.last_name || '',
          bio: user.bio || '',
          phone: user.phone || ''
        };
      }
    });
    
    // Загружаем выбранную группу пользователя
    loadUserGroup();
    
    return () => {
      unsubAuth();
      unsubUser();
    };
  });
  
  async function loadUserGroup() {
    isLoadingGroup = true;
    selectedGroup = await getUserGroup();
    isLoadingGroup = false;
  }
  
  async function handleSearchGroups() {
    if (searchQuery.length >= 2) {
      searchResults = await searchGroups(searchQuery);
      showDropdown = true;
    } else {
      searchResults = [];
      showDropdown = false;
    }
  }
  
  async function handleSelectGroup(group: Group) {
    try {
      isChangingGroup = true;
      changeSuccessful = false;
      showDropdown = false;
      
      const success = await selectUserGroup(group.id);
      
      if (success) {
        // Обновляем выбранную группу в UI
        selectedGroup = group;
        changeSuccessful = true;
        
        console.log('Группа успешно выбрана:', group);
        
        // Скрыть уведомление через 3 секунды
        setTimeout(() => {
          changeSuccessful = false;
        }, 3000);
      } else {
        console.error('Не удалось выбрать группу');
        alert('Не удалось выбрать группу. Пожалуйста, попробуйте еще раз.');
      }
    } catch (error) {
      console.error('Ошибка при выборе группы:', error);
      alert('Произошла ошибка при выборе группы. Пожалуйста, попробуйте позже.');
    } finally {
      isChangingGroup = false;
    }
  }
  
  function toggleEditMode() {
    isEditMode = !isEditMode;
    saveError = '';
    saveSuccess = false;
    
    // Сбрасываем данные до исходных при отмене редактирования
    if (!isEditMode && user) {
      editData = {
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        bio: user.bio || '',
        phone: user.phone || ''
      };
    }
  }
  
  async function saveProfile() {
    if (!user) return;
    
    try {
      isSaving = true;
      saveError = '';
      saveSuccess = false;
      
      // Проверяем обязательные поля
      if (!editData.first_name || !editData.last_name) {
        saveError = 'Имя и фамилия обязательны для заполнения';
        return;
      }
      
      // Отправляем данные на сервер
      const success = await authStore.updateUserProfile(editData);
      
      if (success) {
        saveSuccess = true;
        // Выходим из режима редактирования
        setTimeout(() => {
          isEditMode = false;
          saveSuccess = false;
        }, 2000);
      } else {
        saveError = 'Не удалось обновить профиль. Пожалуйста, попробуйте позже.';
      }
    } catch (error) {
      console.error('Ошибка при обновлении профиля:', error);
      saveError = 'Произошла ошибка при обновлении профиля.';
    } finally {
      isSaving = false;
    }
  }
  
  function handleLogout() {
    authStore.logout();
  }
</script>

<div class="profile-container">
  <header>
    <a href="/" class="back-button">← На главную</a>
    <h1>Профиль пользователя</h1>
    <button class="logout-button" on:click={handleLogout}>Выйти</button>
  </header>
  
  <main>
    {#if isLoading}
      <div class="loading">Загрузка данных профиля...</div>
    {:else if user}
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar-container">
            {#if user.avatar && user.avatar.includes('http')}
              <img src={user.avatar} alt="Фото профиля" class="avatar" />
            {:else}
              <div class="avatar-placeholder">
                {user.first_name.charAt(0)}{user.last_name.charAt(0)}
              </div>
            {/if}
          </div>
          
          <div class="profile-info">
            <h2>{user.first_name} {user.last_name}</h2>
            <p class="username">@{user.username}</p>
            <p class="role">{user.role === 'student' ? 'Студент' : user.role === 'teacher' ? 'Преподаватель' : 'Администратор'}</p>
          </div>
        </div>
        
        <div class="profile-details">
          {#if !isEditMode}
            <!-- Режим просмотра -->
            <div class="detail-item">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{user.email}</span>
            </div>
            
            {#if user.bio}
              <div class="detail-item">
                <span class="detail-label">О себе:</span>
                <span class="detail-value">{user.bio}</span>
              </div>
            {/if}
            
            {#if user.phone}
              <div class="detail-item">
                <span class="detail-label">Телефон:</span>
                <span class="detail-value">{user.phone}</span>
              </div>
            {/if}
          {:else}
            <!-- Режим редактирования -->
            <div class="edit-form">
              <div class="form-group">
                <label for="first_name">Имя</label>
                <input 
                  type="text" 
                  id="first_name" 
                  bind:value={editData.first_name} 
                  placeholder="Введите имя"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="last_name">Фамилия</label>
                <input 
                  type="text" 
                  id="last_name" 
                  bind:value={editData.last_name} 
                  placeholder="Введите фамилию"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="phone">Телефон</label>
                <input 
                  type="tel" 
                  id="phone" 
                  bind:value={editData.phone} 
                  placeholder="Введите номер телефона"
                />
              </div>
              
              <div class="form-group">
                <label for="bio">О себе</label>
                <textarea 
                  id="bio" 
                  bind:value={editData.bio} 
                  placeholder="Расскажите о себе"
                  rows="3"
                ></textarea>
              </div>
              
              {#if saveError}
                <div class="error-message">{saveError}</div>
              {/if}
              
              {#if saveSuccess}
                <div class="success-message">Профиль успешно обновлен!</div>
              {/if}
              
              <div class="edit-actions">
                <button class="cancel-button" on:click={toggleEditMode} disabled={isSaving}>Отмена</button>
                <button class="save-button" on:click={saveProfile} disabled={isSaving}>
                  {isSaving ? 'Сохранение...' : 'Сохранить'}
                </button>
              </div>
            </div>
          {/if}
          
          <!-- Выбор группы для расписания -->
          <div class="detail-item group-selection">
            <span class="detail-label">Группа для расписания:</span>
            
            {#if isLoadingGroup}
              <div class="loading-small">Загрузка...</div>
            {:else if selectedGroup}
              <div class="selected-group">
                <span class="group-info">{selectedGroup.number} {selectedGroup.name ? `(${selectedGroup.name})` : ''}</span>
                <button class="change-group-button" on:click={() => showDropdown = true}>Изменить</button>
              </div>
            {:else}
              <div class="no-group">
                <span>Группа не выбрана</span>
                <button class="select-group-button" on:click={() => showDropdown = true}>Выбрать группу</button>
              </div>
            {/if}
            
            {#if showDropdown}
              <div class="group-search-dropdown">
                <div class="group-search-header">
                  <input 
                    type="text" 
                    placeholder="Введите номер группы..." 
                    bind:value={searchQuery}
                    on:input={handleSearchGroups}
                    autofocus
                  />
                  <button class="close-dropdown" on:click={() => showDropdown = false}>×</button>
                </div>
                
                <div class="group-search-results">
                  {#if searchQuery.length < 2}
                    <div class="search-info">Введите минимум 2 символа для поиска</div>
                  {:else if searchResults.length === 0}
                    <div class="search-info">Группы не найдены</div>
                  {:else}
                    {#each searchResults as group}
                      <button 
                        class="group-result-item" 
                        on:click={() => handleSelectGroup(group)}
                      >
                        {group.number} {group.name ? `(${group.name})` : ''}
                      </button>
                    {/each}
                  {/if}
                </div>
              </div>
            {/if}
            
            {#if changeSuccessful}
              <div class="success-message">Группа успешно выбрана!</div>
            {/if}
          </div>
        </div>
        
        <div class="profile-actions">
          {#if !isEditMode}
            <button class="edit-button" on:click={toggleEditMode}>Редактировать профиль</button>
            <button class="change-password-button">Сменить пароль</button>
          {/if}
        </div>
      </div>
    {:else}
      <div class="error">Не удалось загрузить данные профиля</div>
    {/if}
  </main>
</div>

<style>
  .profile-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    min-height: 100vh;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
  }
  
  .back-button {
    text-decoration: none;
    color: #666;
    font-size: 16px;
    transition: color 0.2s;
  }
  
  .back-button:hover {
    color: #007aff;
  }
  
  h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
  
  .logout-button {
    background: none;
    border: none;
    color: #d32f2f;
    font-size: 16px;
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 5px;
    transition: background-color 0.2s;
  }
  
  .logout-button:hover {
    background-color: #ffeeee;
  }
  
  .loading, .error {
    text-align: center;
    padding: 30px;
    font-size: 18px;
    color: #666;
  }
  
  .error {
    color: #d32f2f;
  }
  
  .profile-card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .profile-header {
    display: flex;
    align-items: center;
    padding: 30px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #eee;
  }
  
  .avatar-container {
    margin-right: 30px;
  }
  
  .avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .avatar-placeholder {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: #007aff;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    font-weight: 600;
    border: 3px solid white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .profile-info h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
  
  .username {
    margin: 5px 0;
    font-size: 16px;
    color: #666;
  }
  
  .role {
    display: inline-block;
    background-color: #007aff;
    color: white;
    padding: 3px 10px;
    border-radius: 15px;
    font-size: 14px;
    margin-top: 5px;
  }
  
  .profile-details {
    padding: 30px;
  }
  
  .detail-item {
    margin-bottom: 15px;
  }
  
  .detail-label {
    font-weight: 600;
    color: #555;
    display: block;
    margin-bottom: 5px;
  }
  
  .detail-value {
    color: #333;
  }
  
  .profile-actions {
    padding: 0 30px 30px;
    display: flex;
    gap: 15px;
  }
  
  .edit-button, .change-password-button {
    padding: 10px 15px;
    border-radius: 5px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .edit-button {
    background-color: #007aff;
    color: white;
    border: none;
  }
  
  .edit-button:hover {
    background-color: #0055cc;
  }
  
  .change-password-button {
    background-color: #f5f5f5;
    color: #555;
    border: 1px solid #ddd;
  }
  
  .change-password-button:hover {
    background-color: #eaeaea;
  }
  
  /* Стили для выбора группы */
  .group-selection {
    position: relative;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #f0f0f0;
  }
  
  .loading-small {
    color: #666;
    font-size: 14px;
    margin-top: 5px;
  }
  
  .selected-group, .no-group {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 5px;
  }
  
  .group-info {
    font-weight: 500;
    color: #444;
  }
  
  .change-group-button, .select-group-button {
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
  }
  
  .change-group-button {
    background-color: #f5f5f5;
    color: #555;
    border: 1px solid #ddd;
  }
  
  .select-group-button {
    background-color: #007aff;
    color: white;
  }
  
  .change-group-button:hover {
    background-color: #eaeaea;
  }
  
  .select-group-button:hover {
    background-color: #0055cc;
  }
  
  .group-search-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    max-width: 400px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    margin-top: 10px;
    z-index: 100;
    overflow: hidden;
  }
  
  .group-search-header {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #eee;
  }
  
  .group-search-header input {
    flex: 1;
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #ddd;
    font-size: 15px;
  }
  
  .close-dropdown {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    padding: 0 10px;
    color: #777;
  }
  
  .group-search-results {
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
  }
  
  .search-info {
    color: #777;
    font-size: 14px;
    text-align: center;
    padding: 15px 0;
  }
  
  .group-result-item {
    display: block;
    width: 100%;
    text-align: left;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    background-color: transparent;
    font-size: 15px;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .group-result-item:hover {
    background-color: #f5f5f5;
  }
  
  .success-message {
    margin-top: 10px;
    padding: 8px 12px;
    background-color: #e7f7e7;
    color: #2c842c;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .edit-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  .form-group label {
    font-size: 14px;
    font-weight: 500;
    color: #666;
  }
  
  .form-group input, .form-group textarea {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
    width: 100%;
  }
  
  .error-message {
    color: #d32f2f;
    font-size: 14px;
    margin-top: 10px;
  }
  
  .edit-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
  }
  
  .cancel-button {
    padding: 10px 20px;
    background-color: #f5f5f5;
    color: #666;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
  }
  
  .save-button {
    padding: 10px 20px;
    background-color: #294380;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
  }
  
  .cancel-button:hover {
    background-color: #e0e0e0;
  }
  
  .save-button:hover {
    background-color: #1a2a50;
  }
  
  .cancel-button:disabled, .save-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .profile-header {
      flex-direction: column;
      text-align: center;
    }
    
    .avatar-container {
      margin: 0 0 20px 0;
    }
    
    .profile-actions {
      flex-direction: column;
    }
    
    .edit-button, .change-password-button {
      width: 100%;
    }
    
    .group-search-dropdown {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 90%;
      max-width: none;
      max-height: 80vh;
      margin: 0;
    }
  }
</style> 