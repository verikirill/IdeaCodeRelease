<script>
  import { onMount } from 'svelte';
  
  let avatar = '/account_photo.png';
  let selectedFrame = null;
  let userName = 'Джанстей';
  let userEmail = 'janstay_ux@gmail.com';
  let editingName = false;
  let editingEmail = false;
  let oldPassword = '';
  let newPassword = '';
  let confirmPassword = '';
  let showOldPassword = false;
  let showNewPassword = false;
  let showConfirmPassword = false;
  let incognitoMode = false;
  let physcoins = 100; // User's balance
  let showPurchaseModal = false;
  let selectedFrameToPurchase = null;
  
  // Frames available for selection
  const frames = [
    { id: 'purple', color: '#9966cc', image: '/account_circle_p.png', owned: true, price: 0 },
    { id: 'pink', color: '#ff66b2', image: '/account_circle_pink.png', owned: false, price: 20 },
    { id: 'blue', color: '#3399ff', image: '/account_circle_b.png', owned: false, price: 20 }
  ];
  
  function toggleEditName() {
    editingName = !editingName;
  }
  
  function toggleEditEmail() {
    editingEmail = !editingEmail;
  }
  
  function saveChanges() {
    // Would handle saving changes to the server
    editingName = false;
    editingEmail = false;
  }
  
  function togglePasswordVisibility(field) {
    const inputId = field + '-password';
    const input = document.getElementById(inputId);
    
    if (!input) return;
    
    // Save cursor position
    const cursorPosition = input.selectionStart;
    
    // Toggle the input type
    input.type = input.type === 'password' ? 'text' : 'password';
    
    // Update state variable
    if (field === 'old') {
      showOldPassword = input.type === 'text';
    } else if (field === 'new') {
      showNewPassword = input.type === 'text';
    } else if (field === 'confirm') {
      showConfirmPassword = input.type === 'text';
    }
    
    // Restore cursor position
    input.setSelectionRange(cursorPosition, cursorPosition);
    input.focus();
  }
  
  function selectFrame(frameId) {
    // Only allow selection if the frame is owned
    const frame = frames.find(f => f.id === frameId);
    if (frame && frame.owned) {
      selectedFrame = frameId;
    } else if (frame && !frame.owned) {
      openPurchaseModal(frameId);
    }
  }
  
  function openPurchaseModal(frameId) {
    selectedFrameToPurchase = frameId;
    showPurchaseModal = true;
  }
  
  function closePurchaseModal() {
    showPurchaseModal = false;
    selectedFrameToPurchase = null;
  }
  
  function purchaseFrame() {
    const frameIndex = frames.findIndex(f => f.id === selectedFrameToPurchase);
    if (frameIndex !== -1) {
      const frame = frames[frameIndex];
      
      if (physcoins >= frame.price) {
        // Update the frame to be owned
        frames[frameIndex].owned = true;
        
        // Deduct coins
        physcoins -= frame.price;
        
        // Select the frame
        selectedFrame = selectedFrameToPurchase;
        
        // Close the modal
        closePurchaseModal();
      }
    }
  }
  
  onMount(() => {
    // Any initialization code
  });
</script>

<div class="page-container">
  <div class="container">
    <!-- Removed the header/navbar section -->
    
    <!-- Removed the profile icon section since it's already in the layout -->

    <main>
      <h1 class="account-title">Личный кабинет</h1>
      
      <div class="account-content">
        <!-- Settings Section -->
        <section class="account-section">
          <h2>Настройки</h2>
          <p class="section-description">
            В данном разделе предоставляются возможности для настройки имени, изменения 
            пароля и других параметров.
          </p>
          <button class="save-button" on:click={saveChanges}>Сохранить изменения</button>
        </section>
        
        <!-- Avatar Section -->
        <section class="account-section">
          <h2>Аватарка профиля</h2>
          <div class="avatar-container">
            <div class="avatar-preview">
              <img src={avatar} alt="Аватар профиля" class="profile-image" />
              {#if selectedFrame}
                <img src={frames.find(f => f.id === selectedFrame)?.image} alt="Рамка" class="frame-image" />
              {/if}
            </div>
          </div>
        </section>
        
        <!-- Frames Section -->
        <section class="account-section">
          <h2>Добавить рамку</h2>
          <div class="physcoins-balance">
            Ваш баланс: <span class="physcoins-amount">{physcoins} <img src="/phys_coins.png" alt="физкоинов" class="physcoin-icon" /></span>
          </div>
          <div class="frames-container">
            {#each frames as frame}
              <div 
                class="frame-option" 
                class:selected={selectedFrame === frame.id}
                class:unavailable={!frame.owned}
                on:click={() => selectFrame(frame.id)}
              >
                <div class="frame-preview">
                  <img src={frame.image} alt="Аватар с рамкой" />
                  {#if !frame.owned}
                    <div class="frame-price">
                      {frame.price} <img src="/phys_coins.png" alt="физкоинов" class="price-coin" />
                    </div>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </section>
        
        <!-- Account Info Section -->
        <section class="account-section">
          <h2>Информация аккаунта</h2>
          <div class="info-container">
            <div class="info-row">
              <div class="info-label">Имя</div>
              {#if editingName}
                <input type="text" class="info-input" bind:value={userName} />
              {:else}
                <div class="info-value">{userName}</div>
              {/if}
              <button class="edit-button" on:click={toggleEditName}>
                {editingName ? 'Сохранить' : 'Изменить'}
              </button>
            </div>
            
            <div class="info-row">
              <div class="info-label">Почта</div>
              {#if editingEmail}
                <input type="email" class="info-input" bind:value={userEmail} />
              {:else}
                <div class="info-value">{userEmail}</div>
              {/if}
              <button class="edit-button" on:click={toggleEditEmail}>
                {editingEmail ? 'Сохранить' : 'Изменить'}
              </button>
            </div>
          </div>
        </section>
        
        <!-- Password Change Section -->
        <section class="account-section">
          <h2>Изменить пароль</h2>
          <div class="password-container">
            <div class="password-row">
              <label for="old-password">Старый пароль</label>
              <div class="password-input-container">
                <input 
                  id="old-password"
                  type="password"
                  placeholder="Введите пароль"
                  bind:value={oldPassword}
                />
                <button 
                  type="button" 
                  class="password-toggle" 
                  on:click={() => togglePasswordVisibility('old')}
                >
                  <svg viewBox="0 0 24 24" width="18" height="18">
                    {#if showOldPassword}
                      <path fill="currentColor" d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
                    {:else}
                      <path fill="currentColor" d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z" />
                    {/if}
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="password-row">
              <label for="new-password">Новый пароль</label>
              <div class="password-input-container">
                <input 
                  id="new-password"
                  type="password"
                  placeholder="Введите пароль"
                  bind:value={newPassword}
                />
                <button 
                  type="button" 
                  class="password-toggle" 
                  on:click={() => togglePasswordVisibility('new')}
                >
                  <svg viewBox="0 0 24 24" width="18" height="18">
                    {#if showNewPassword}
                      <path fill="currentColor" d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
                    {:else}
                      <path fill="currentColor" d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z" />
                    {/if}
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="password-row">
              <label for="confirm-password">Повторите пароль</label>
              <div class="password-input-container">
                <input 
                  id="confirm-password"
                  type="password"
                  placeholder="Введите пароль"
                  bind:value={confirmPassword}
                />
                <button 
                  type="button" 
                  class="password-toggle" 
                  on:click={() => togglePasswordVisibility('confirm')}
                >
                  <svg viewBox="0 0 24 24" width="18" height="18">
                    {#if showConfirmPassword}
                      <path fill="currentColor" d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
                    {:else}
                      <path fill="currentColor" d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z" />
                    {/if}
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </section>
        
        <!-- Incognito Mode Section -->
        <section class="account-section">
          <div class="incognito-row">
            <span class="incognito-label">Режим инкогнито</span>
            <label class="toggle-switch">
              <input type="checkbox" bind:checked={incognitoMode}>
              <span class="toggle-slider"></span>
            </label>
          </div>
        </section>
      </div>
    </main>
  </div>
</div>

<!-- Purchase Modal -->
{#if showPurchaseModal}
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Купить рамку</h3>
        <button class="close-button" on:click={closePurchaseModal}>✕</button>
      </div>
      
      {#if selectedFrameToPurchase}
        {@const frame = frames.find(f => f.id === selectedFrameToPurchase)}
        {#if frame}
          <div class="modal-body">
            <div class="purchase-frame-preview">
              <img src={frame.image} alt="Рамка" />
            </div>
            
            <div class="purchase-details">
              <div class="purchase-info">
                <div class="purchase-label">Сумма покупки</div>
                <div class="purchase-value">{frame.price} <img src="/phys_coins.png" alt="физкоинов" class="price-coin" /></div>
              </div>
              
              <div class="purchase-info">
                <div class="purchase-label">Ваш баланс</div>
                <div class="purchase-value">{physcoins} <img src="/phys_coins.png" alt="физкоинов" class="price-coin" /></div>
              </div>
              
              {#if physcoins < frame.price}
                <div class="insufficient-funds">
                  <h4>У вас нет физкоинов?</h4>
                  <p>
                    Заработать физкоины можно за активность на платформе (комментарии, посты, лайки) за каждое действие - 1 физкоин
                  </p>
                  <button class="services-button" on:click={() => window.location.href = '/'}>
                    Перейти к сервисам
                  </button>
                </div>
              {/if}
            </div>
          </div>
          
          <div class="modal-footer">
            <button 
              class="purchase-button" 
              disabled={physcoins < frame.price}
              on:click={purchaseFrame}
            >
              Купить рамку
            </button>
          </div>
        {/if}
      {/if}
    </div>
  </div>
{/if}

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

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'SF Pro Display', Arial, sans-serif;
    min-height: 100vh;
  }
  
  .page-container {
    width: 100%;
    min-height: 100vh;
    position: relative;
  }
  
  .page-container::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('/account_background.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    z-index: -1;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Navbar */
  .navbar {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
  }

  .nav-buttons {
    display: flex;
    gap: 15px;
  }

  .nav-button {
    background-color: #f0f0f0;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
  }

  .nav-button:hover {
    background-color: #e0e0e0;
  }

  .icon {
    font-size: 18px;
    display: flex;
    align-items: center;
  }

  .icon img {
    width: 18px;
    height: 18px;
  }

  .nav-link {
    text-decoration: none;
    color: inherit;
  }

  /* Profile */
  .profile {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 100;
  }

  .profile-link {
    display: block;
    text-decoration: none;
  }

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    background-color: #fff;
  }

  .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Account content styles */
  .account-title {
    font-size: 36px;
    margin: 40px 0;
    color: #000;
    text-align: left;
    padding-left: 20px;
    font-weight: 500;
  }

  .account-content {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-bottom: 60px;
  }

  .account-section {
    background-color: #fff;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }

  .account-section h2 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 22px;
  }

  .section-description {
    color: #666;
    margin-bottom: 20px;
    line-height: 1.5;
  }

  .save-button {
    background-color: #e0e0e0;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
  }

  .save-button:hover {
    background-color: #d0d0d0;
  }

  /* Avatar styles */
  .avatar-container {
    display: flex;
    justify-content: flex-start;
  }

  .avatar-preview {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: visible;
    background-color: #fff;
    position: relative;
  }

  .avatar-preview .profile-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
  }
  
  .avatar-preview .frame-image {
    width: 140px;
    height: 140px;
    position: absolute;
    top: -10px;
    left: -10px;
    z-index: 1;
    object-fit: contain;
  }

  /* Frames styles */
  .frames-container {
    display: flex;
    gap: 20px;
  }

  .frame-option {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: visible;
    cursor: pointer;
    position: relative;
  }

  .frame-preview {
    width: 100%;
    height: 100%;
    position: relative;
  }

  .frame-preview img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .frame-option.selected {
    box-shadow: 0 0 0 2px #000;
  }

  /* Info styles */
  .info-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .info-row {
    display: flex;
    align-items: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
  }

  .info-label {
    flex: 0 0 70px;
    color: #666;
  }

  .info-value {
    flex: 1;
  }

  .info-input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .edit-button {
    background-color: transparent;
    border: none;
    color: #3399ff;
    cursor: pointer;
    margin-left: 15px;
  }

  /* Password styles */
  .password-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .password-row {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .password-row label {
    color: #666;
  }

  .password-input-container {
    position: relative;
    display: flex;
    align-items: center;
  }

  .password-input-container input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
  }

  .password-toggle {
    position: absolute;
    right: 10px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    color: #999;
  }

  .password-toggle:hover {
    color: #666;
  }

  /* Incognito styles */
  .incognito-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .incognito-label {
    font-weight: 500;
  }

  .toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
  }

  .toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 34px;
  }

  .toggle-slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }

  input:checked + .toggle-slider {
    background-color: #1A3882;
  }

  input:checked + .toggle-slider:before {
    transform: translateX(26px);
  }

  @media (max-width: 768px) {
    .account-content {
      padding: 0 10px;
    }
    
    .nav-buttons {
      width: 100%;
      justify-content: center;
    }
    
    .frames-container {
      justify-content: space-between;
    }
  }

  /* PhysCoins styles */
  .physcoins-balance {
    margin-bottom: 15px;
    font-weight: 500;
    display: flex;
    align-items: center;
  }
  
  .physcoins-amount {
    color: #1A3882;
    font-weight: bold;
    display: flex;
    align-items: center;
    margin-left: 5px;
  }

  .physcoin-icon {
    width: 20px;
    height: 20px;
    margin-left: 5px;
  }
  
  /* Frame price styles */
  .frame-option.unavailable {
    opacity: 0.9;
    cursor: pointer;
  }
  
  .frame-price {
    position: absolute;
    bottom: -8px;
    right: -8px;
    background-color: #1A3882;
    color: white;
    border-radius: 20px;
    height: 24px;
    padding: 0 5px 0 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
  }
  
  .price-coin {
    width: 16px;
    height: 16px;
    margin-left: 3px;
  }
  
  /* Modal styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: #f5f5f5;
    border-radius: 15px;
    width: 90%;
    max-width: 420px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    position: relative;
  }
  
  .modal-header {
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .modal-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
  }
  
  .close-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #888;
    position: absolute;
    right: 10px;
    top: 10px;
  }
  
  .modal-body {
    padding: 0 20px 20px;
  }
  
  .purchase-frame-preview {
    display: flex;
    justify-content: center;
    margin-bottom: 25px;
    position: relative;
  }
  
  .purchase-frame-preview::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: url('/phys_coin.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    opacity: 0.15;
    z-index: -1;
  }
  
  .purchase-frame-preview img {
    width: 180px;
    height: 180px;
    object-fit: contain;
  }
  
  .purchase-details {
    margin-bottom: 20px;
  }
  
  .purchase-info {
    background-color: white;
    border-radius: 10px;
    padding: 12px 15px;
    margin-bottom: 10px;
  }
  
  .purchase-label {
    color: #666;
    font-size: 14px;
    margin-bottom: 5px;
  }
  
  .purchase-value {
    font-weight: 600;
    font-size: 16px;
    display: flex;
    align-items: center;
  }
  
  .purchase-value::after {
    content: "";
    display: inline-block;
    width: 20px;
    height: 20px;
    background-image: url('/phys_coin.png');
    background-size: contain;
    background-repeat: no-repeat;
    margin-left: 5px;
  }
  
  .insufficient-funds {
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 15px;
    margin-top: 20px;
  }
  
  .insufficient-funds h4 {
    margin: 0 0 10px 0;
    font-size: 16px;
    font-weight: 600;
  }
  
  .insufficient-funds p {
    color: #666;
    font-size: 14px;
    line-height: 1.4;
    margin-bottom: 15px;
  }
  
  .services-button {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 40px;
    padding: 12px 20px;
    width: 100%;
    font-size: 16px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  .modal-footer {
    padding: 0 0 15px 0;
  }
  
  .purchase-button {
    background-color: #ff66b2;
    color: white;
    border: none;
    border-radius: 40px;
    padding: 14px;
    margin: 0 20px;
    width: calc(100% - 40px);
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 3px 10px rgba(255, 102, 178, 0.3);
  }
  
  .purchase-button:disabled {
    background-color: #ccc;
    box-shadow: none;
    cursor: not-allowed;
  }
  
  .coin-icon {
    display: none;
  }
</style> 