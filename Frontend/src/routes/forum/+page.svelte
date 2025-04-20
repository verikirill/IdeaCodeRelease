<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  interface Comment {
    id: number;
    content: string;
    author: {
      id: number;
      username: string;
    };
    created_at: string;
  }
  
  interface Post {
    id: number;
    title: string;
    content: string;
    photo_url?: string;
    category: string;
    author: {
      id: number;
      username: string;
    };
    likes: any[];
    comments: Comment[];
    created_at: string;
    updated_at: string;
  }
  
  const API_URL = 'http://localhost:8000';
  let avatar = '/avatar.png';
  let showNewPostForm = false;
  let isLoading = true;
  let error = '';
  let isLoggedIn = false;
  let authError = '';
  
  let posts: Post[] = [];
  let newPostTitle = '';
  let newPostContent = '';
  let newPostCategory = 'FLOOD';
  let newPostImage: File | null = null;

  let newCommentText = '';
  
  let selectedPost: Post | null = null;
  
  function viewPost(post: Post): void {
    selectedPost = selectedPost?.id === post.id ? null : post;
  }
  
  function toggleNewPostForm(): void {
    if (!isLoggedIn) {
      authError = 'Пожалуйста, войдите в систему, чтобы создать запись';
      return;
    }
    
    authError = '';
    showNewPostForm = !showNewPostForm;
  }

  // Get auth token from localStorage
  function getAuthToken(): string | null {
    if (browser) {
      return localStorage.getItem('token');
    }
    return null;
  }

  // Check if user is logged in
  function checkAuth(): boolean {
    const token = getAuthToken();
    return token !== null && token !== '';
  }

  // Get headers with auth token
  function getAuthHeaders(): Headers {
    const headers = new Headers();
    const token = getAuthToken();
    
    if (token) {
      headers.append('Authorization', `Bearer ${token}`);
    }
    
    return headers;
  }

  async function fetchPosts() {
    try {
      isLoading = true;
      const response = await fetch(`${API_URL}/posts`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      posts = data;
    } catch (err) {
      console.error('Error fetching posts:', err);
      error = 'Не удалось загрузить посты. Пожалуйста, попробуйте позже.';
    } finally {
      isLoading = false;
    }
  }

  async function handleSubmitPost() {
    try {
      if (!isLoggedIn) {
        authError = 'Пожалуйста, войдите в систему, чтобы создать запись';
        return;
      }
      
      if (!newPostTitle || !newPostContent) {
        alert('Пожалуйста, заполните все поля');
        return;
      }

      const headers = getAuthHeaders();
      
      if (newPostImage) {
        const formData = new FormData();
        formData.append('title', newPostTitle);
        formData.append('content', newPostContent);
        formData.append('category', newPostCategory);
        formData.append('file', newPostImage);
        
        const response = await fetch(`${API_URL}/posts/upload`, {
          method: 'POST',
          body: formData,
          headers: headers,
          credentials: 'include',
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            authError = 'Необходимо войти в систему. Пожалуйста, авторизуйтесь.';
            return;
          }
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      } else {
        // Set content type only when sending JSON
        headers.append('Content-Type', 'application/json');
        
        const response = await fetch(`${API_URL}/posts`, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({
            title: newPostTitle,
            content: newPostContent,
            category: newPostCategory,
          }),
          credentials: 'include',
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            authError = 'Необходимо войти в систему. Пожалуйста, авторизуйтесь.';
            return;
          }
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      }
      
      // Reset form and refresh posts
      newPostTitle = '';
      newPostContent = '';
      newPostCategory = 'FLOOD';
      newPostImage = null;
      showNewPostForm = false;
      authError = '';
      
      await fetchPosts();
    } catch (err) {
      console.error('Error creating post:', err);
      alert('Не удалось создать пост. Пожалуйста, попробуйте позже.');
    }
  }

  async function handleSubmitComment(postId: number) {
    try {
      if (!isLoggedIn) {
        authError = 'Пожалуйста, войдите в систему, чтобы добавить комментарий';
        return;
      }
      
      if (!newCommentText) {
        return;
      }

      const headers = getAuthHeaders();
      headers.append('Content-Type', 'application/json');
      
      const response = await fetch(`${API_URL}/posts/${postId}/comments`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          content: newCommentText,
        }),
        credentials: 'include',
      });

      if (!response.ok) {
        if (response.status === 401) {
          authError = 'Необходимо войти в систему. Пожалуйста, авторизуйтесь.';
          return;
        }
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      newCommentText = '';
      authError = '';
      await fetchPosts();
      
      // Update the selected post with the latest data
      if (selectedPost) {
        const postResponse = await fetch(`${API_URL}/posts/${postId}`);
        if (postResponse.ok) {
          const updatedPost = await postResponse.json();
          selectedPost = updatedPost;
        }
      }
    } catch (err) {
      console.error('Error adding comment:', err);
      alert('Не удалось добавить комментарий. Пожалуйста, попробуйте позже.');
    }
  }

  async function handleLikePost(postId: number) {
    try {
      if (!isLoggedIn) {
        authError = 'Пожалуйста, войдите в систему, чтобы поставить лайк';
        return;
      }
      
      const headers = getAuthHeaders();
      
      const response = await fetch(`${API_URL}/posts/${postId}/like`, {
        method: 'POST',
        headers: headers,
        credentials: 'include',
      });

      if (!response.ok) {
        if (response.status === 401) {
          authError = 'Необходимо войти в систему. Пожалуйста, авторизуйтесь.';
          return;
        }
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      authError = '';
      await fetchPosts();
      
      // Update the selected post
      if (selectedPost && selectedPost.id === postId) {
        const postResponse = await fetch(`${API_URL}/posts/${postId}`);
        if (postResponse.ok) {
          selectedPost = await postResponse.json();
        }
      }
    } catch (err) {
      console.error('Error liking post:', err);
    }
  }

  function handleFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      newPostImage = input.files[0];
    }
  }

  function formatDate(dateString: string): string {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ru-RU', {
      day: 'numeric',
      month: 'long'
    }).format(date);
  }
  
  onMount(() => {
    // Check authentication status
    isLoggedIn = checkAuth();
    fetchPosts();
  });
</script>

<div class="forum-page"></div>
<div class="forum-content">
  <div class="container">
    <main>
      <div class="forum-header">
        <h1>Студенческий форум</h1>
        <p>{posts.length} {posts.length === 1 ? 'запись' : posts.length >= 2 && posts.length <= 4 ? 'записи' : 'записей'}</p>
      </div>

      {#if authError}
        <div class="auth-error">
          {authError}
          <a href="/login" class="login-link">Войти в систему</a>
        </div>
      {/if}

      <div class="content">
        <div class="left-panel">
          <div class="section-header">
            <span class="section-icon"><img src="/3lines.svg" alt="Menu" /></span>
            <h2>Записи</h2>
          </div>

          {#if isLoading}
            <div class="loading">Загрузка постов...</div>
          {:else if error}
            <div class="error">{error}</div>
          {:else if posts.length === 0}
            <div class="no-posts">Пока нет записей в форуме</div>
          {:else}
            <div class="posts">
              {#each posts as post}
                <!-- Expanded view for selected post -->
                {#if selectedPost && selectedPost.id === post.id}
                  <div class="post selected-post">
                    <div class="user-avatar"></div>
                    <div class="post-content">
                      {#if post.photo_url}
                        <div class="post-image-container">
                          <img src={post.photo_url} alt={post.title} class="post-image" />
                        </div>
                      {:else}
                        <div class="post-image-container">
                          <div class="post-image-placeholder"></div>
                        </div>
                      {/if}
                      <h3 class="post-title">{post.title}</h3>
                      <p class="post-text">{post.content}</p>
                      <div class="post-meta">
                        <span class="meta-item date">
                          <img src="/mdi_calendar.svg" alt="Дата" /> {formatDate(post.created_at)}
                        </span>
                        <span class="meta-item author">
                          <img src="/user-icon.svg" alt="Автор" /> {post.author?.username || 'Аноним'}
                        </span>
                        <span class="meta-item likes" on:click={() => handleLikePost(post.id)}>
                          <img src="main_page/like.svg" alt="Лайки" /> {post.likes?.length || 0}
                        </span>
                        <span class="meta-item replies">
                          <img src="/otvet.svg" alt="Ответы" /> {post.comments?.length || 0} 
                          {post.comments?.length === 1 ? 'ответ' : 
                           post.comments?.length >= 2 && post.comments?.length <= 4 ? 'ответа' : 'ответов'}
                        </span>
                      </div>
                      
                      <button class="view-replies collapse" on:click={() => viewPost(post)}>Свернуть ответы</button>
                      
                      <!-- Comments -->
                      <div class="post-comments">
                        {#if post.comments && post.comments.length > 0}
                          {#each post.comments as comment}
                            <div class="comment">
                              <div class="user-avatar"></div>
                              <div class="comment-content">
                                <h4 class="comment-author">{comment.author?.username || 'Аноним'}</h4>
                                <p class="comment-text">{comment.content}</p>
                                <div class="comment-date">{formatDate(comment.created_at)}</div>
                              </div>
                            </div>
                          {/each}
                        {:else}
                          <div class="no-comments">
                            <p>Пока нет комментариев</p>
                          </div>
                        {/if}

                        <!-- Comment form -->
                        <div class="add-comment-form">
                          <textarea 
                            bind:value={newCommentText} 
                            placeholder="Добавить комментарий..."
                          ></textarea>
                          <button on:click={() => handleSubmitComment(post.id)}>Отправить</button>
                        </div>
                      </div>
                    </div>
                  </div>
                {:else}
                  <!-- Collapsed view for other posts -->
                  <div class="post">
                    <div class="user-avatar"></div>
                    <div class="post-content">
                      {#if post.photo_url}
                        <div class="post-image-container">
                          <img src={post.photo_url} alt={post.title} class="post-image" />
                        </div>
                      {:else}
                        <div class="post-image-container">
                          <div class="post-image-placeholder"></div>
                        </div>
                      {/if}
                      <h3 class="post-title">{post.title}</h3>
                      <div class="post-meta">
                        <span class="meta-item date">
                          <img src="/mdi_calendar.svg" alt="Дата" /> {formatDate(post.created_at)}
                        </span>
                        <span class="meta-item author">
                          <img src="/user-icon.svg" alt="Автор" /> {post.author?.username || 'Аноним'}
                        </span>
                        <span class="meta-item likes" on:click={() => handleLikePost(post.id)}>
                          <img src="main_page/like.svg" alt="Лайки" /> {post.likes?.length || 0}
                        </span>
                        <span class="meta-item replies">
                          <img src="/otvet.svg" alt="Ответы" /> {post.comments?.length || 0}
                          {post.comments?.length === 1 ? 'ответ' : 
                           post.comments?.length >= 2 && post.comments?.length <= 4 ? 'ответа' : 'ответов'}
                        </span>
                      </div>
                      <button class="view-replies" on:click={() => viewPost(post)}>Смотреть подробнее</button>
                    </div>
                  </div>
                {/if}
              {/each}
            </div>
          {/if}
        </div>

        <div class="right-panel">
          <div class="about-forum">
            <div class="section-header">
              <span class="section-icon"><img src="/3lines.svg" alt="Menu" /></span>
              <h2>О форуме</h2>
            </div>
            
            <div class="info-block">
              <span class="info-icon">
                <img src="/info.svg" alt="Информация" />
              </span>
              <p>Добро пожаловать на Студенческий Хаб — место, где встречаются знания, опыт и студенческая жизнь!</p>
            </div>
            
            <p class="about-text">
              Неважно, первокурсник ты или выпускник – здесь каждый найдёт что-то полезное (и забавное).
              Присоединяйся, задавай вопросы, делись опытом и делай студенческие годы ярче!
            </p>
          </div>

          <div class="topics">
            <div class="section-header">
              <span class="section-icon"><img src="/3lines.svg" alt="Menu" /></span>
              <h2>Темы</h2>
            </div>
            
            <div class="topic-icons">
              <div class="topic" on:click={() => newPostCategory = 'FLOOD'}>
                <div class="topic-icon {newPostCategory === 'FLOOD' ? 'active' : ''}">
                  <img src="/cute house.png" alt="Флудилка" class="icon-house" />
                </div>
                <span>Флудилка</span>
              </div>
              <div class="topic" on:click={() => newPostCategory = 'LOST_FOUND'}>
                <div class="topic-icon {newPostCategory === 'LOST_FOUND' ? 'active' : ''}">
                  <img src="/search cute blue icon.png" alt="Потеряшки" class="icon-search" />
                </div>
                <span>Потеряшки</span>
              </div>
              <div class="topic" on:click={() => newPostCategory = 'OVERHEARD'}>
                <div class="topic-icon {newPostCategory === 'OVERHEARD' ? 'active' : ''}">
                  <img src="/blue speech bubble.png" alt="Подслушано" class="icon-speech" />
                </div>
                <span>Подслушано</span>
              </div>
              <div class="topic" on:click={() => newPostCategory = 'NOTES'}>
                <div class="topic-icon {newPostCategory === 'NOTES' ? 'active' : ''}">
                  <img src="/cute books.png" alt="Конспекты" class="icon-books" />
                </div>
                <span>Конспекты</span>
              </div>
              <div class="topic" on:click={() => newPostCategory = 'USEFUL'}>
                <div class="topic-icon {newPostCategory === 'USEFUL' ? 'active' : ''}">
                  <img src="/thumbs up.png" alt="Полезное" class="icon-thumbs" />
                </div>
                <span>Полезное</span>
              </div>
            </div>
          </div>
          
          <div class="add-post-container">
            <button class="add-post-button" on:click={toggleNewPostForm}>
              <span class="add-icon">+</span>
              Добавить запись
            </button>
            
            {#if showNewPostForm}
            <div class="new-post-form">
              <h2>Новый пост</h2>
              <p class="form-subtitle">Заполните поля ниже</p>
              
              <div class="form-group">
                <label>Заголовок</label>
                <input type="text" bind:value={newPostTitle} placeholder="Введите заголовок" />
              </div>
              
              <div class="form-group">
                <label>Файл поста</label>
                <div class="file-upload">
                  <input type="file" id="post-image" on:change={handleFileChange} accept="image/*" />
                  <label for="post-image" class="file-upload-label">
                    <div class="camera-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                        <circle cx="12" cy="13" r="4"></circle>
                      </svg>
                    </div>
                    {newPostImage ? newPostImage.name : 'Добавить изображение'}
                  </label>
                </div>
              </div>
              
              <div class="form-group">
                <label>Описание к посту</label>
                <textarea bind:value={newPostContent} placeholder="Текст"></textarea>
              </div>
              
              <button class="publish-button" on:click={handleSubmitPost}>
                Опубликовать запись
              </button>
            </div>
            {/if}
          </div>
        </div>
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
    background-color: #ffffff;
  }

  /* Фон страницы */
  .forum-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    z-index: -1;
  }
  
  .forum-content {
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

  .icon {
    font-size: 18px;
    display: flex;
    align-items: center;
  }

  .icon img {
    width: 18px;
    height: 18px;
  }

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #333;
  }

  .profile {
    position: fixed;
    top: 20px;
    right: 20px;
  }

  /* Forum Header */
  .forum-header {
    margin: 40px 0;
    text-align: center;
  }

  .forum-header h1 {
    font-size: 32px;
    margin-bottom: 10px;
  }

  .forum-header p {
    color: #666;
    margin: 0;
  }

  /* Content Layout */
  .content {
    display: flex;
    gap: 20px;
  }

  .left-panel {
    flex: 1.5;
    background-color: #F0F0F0;
    border-radius: 15px;
    padding: 20px;
  }

  .right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .about-forum, .topics {
    background-color: #F0F0F0;
    border-radius: 15px;
    padding: 15px;
  }

  /* Topics */
  .topics {
    padding: 15px;
  }

  /* Section Headers */
  .left-panel .section-header,
  .about-forum .section-header,
  .topics .section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
    background-color: #1A3882;
    padding: 6px 12px;
    border-radius: 10px;
    width: fit-content;
  }

  .left-panel .section-header h2,
  .left-panel .section-header .section-icon,
  .about-forum .section-header h2,
  .about-forum .section-header .section-icon,
  .topics .section-header h2,
  .topics .section-header .section-icon {
    color: #fff;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    background-color: #c0c0c0;
    padding: 8px 15px;
    border-radius: 12px;
    width: fit-content;
  }

  .section-icon {
    display: flex;
    align-items: center;
  }

  .section-icon img {
    width: 18px;
    height: 18px;
  }

  .section-header h2 {
    font-size: 16px;
    margin: 0;
    font-weight: normal;
  }

  /* Posts */
  .posts {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .post {
    display: flex;
    gap: 8px;
  }
  
  .selected-post {
    cursor: default;
  }

  .user-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #ffffff;
    flex-shrink: 0;
    margin-top: 5px;
  }

  .post-content {
    flex: 1;
    position: relative;
    padding-left: 5px;
  }

  .post-image-container {
    display: flex;
    justify-content: flex-start;
    width: 100%;
  }

  .post-image-placeholder {
    width: 70%;
    height: 150px;
    background-color: #ffffff;
    border-radius: 10px;
    margin-bottom: 15px;
  }

  .post-title {
    font-size: 18px;
    margin: 0 0 15px 0;
    font-weight: normal;
    text-align: left;
  }

  .post-meta {
    display: flex;
    gap: 15px;
    margin-bottom: 15px;
    color: #888;
    font-size: 14px;
    align-items: center;
  }
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .meta-item img {
    width: 18px;
    height: 18px;
  }

  .view-replies {
    background-color: #1A3882;
    border: none;
    border-radius: 12px;
    padding: 8px 0;
    width: 45%;
    cursor: pointer;
    font-size: 14px;
    color: #fff;
    text-align: center;
    margin-left: 10%;
  }

  /* Topics */
  .topic-icons {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    gap: 10px;
  }

  .topic {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }

  .topic-icon {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #c0c0c0;
  }

  .topic-icon img {
    max-width: 100%;
    max-height: 100%;
  }

  /* Custom icon sizes with higher specificity */
  .topic-icon .icon-house {
    width: 48px !important;
    height: 38px !important;
  }

  .topic-icon .icon-search {
    width: 38px !important;
    height: 37px !important;
  }

  .topic-icon .icon-speech {
    width: 41px !important;
    height: 57px !important;
  }

  .topic-icon .icon-books {
    width: 40px !important;
    height: 40px !important;
  }

  .topic-icon .icon-thumbs {
    width: 35px !important;
    height: 40px !important;
  }

  /* Info Block */
  .info-block {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
  }

  .info-icon {
    font-size: 22px;
    display: flex;
    align-items: center;
  }

  .info-icon img {
    width: 16px;
    height: 16px;
  }

  .about-text {
    margin: 0;
    line-height: 1.4;
    color: #333;
    font-size: 14px;
  }

  /* Post Comments */
  .post-comments {
    margin-top: 10px;
    border-top: 1px solid #ccc;
    padding-top: 20px;
  }
  
  .comment {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
  }
  
  .comment-content {
    background-color: #fff;
    border-radius: 10px;
    padding: 15px;
    flex: 1;
  }
  
  .comment-author {
    font-size: 16px;
    margin: 0 0 10px 0;
    font-weight: bold;
  }
  
  .comment-text {
    font-size: 14px;
    margin: 0;
    line-height: 1.4;
  }

  .nav-link {
    text-decoration: none;
  }

  .nav-button.active {
    background-color: #e0e0e0;
  }
  
  /* Add Post Button */
  .add-post-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-top: 5px;
    position: relative;
  }
  
  .add-post-button {
    display: flex;
    align-items: center;
    background-color: #294380;
    color: white;
    border: none;
    border-radius: 20px;
    font-size: 16px;
    font-weight: 500;
    padding: 12px 24px;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease;
  }
  
  .add-post-button:hover {
    background-color: #1A3070;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .add-icon {
    font-size: 20px;
    margin-right: 8px;
    font-weight: bold;
  }

  /* New Post Form */
  .new-post-form {
    background-color: #fff;
    width: 100%;
    border-radius: 20px;
    padding: 25px;
    margin-top: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    z-index: 10;
  }

  .new-post-form h2 {
    margin: 0 0 5px 0;
    font-size: 28px;
    font-weight: 600;
  }

  .form-subtitle {
    color: #666;
    margin: 0 0 25px 0;
    font-size: 16px;
  }

  .form-group {
    margin-bottom: 25px;
  }

  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 10px;
    font-size: 18px;
  }

  .file-upload {
    width: 100px;
    height: 100px;
    background-color: #E8E8E8;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .camera-icon {
    color: #6C81A6;
  }

  textarea {
    width: 100%;
    height: 120px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-family: 'SF Pro Display', Arial, sans-serif;
    font-size: 16px;
    resize: none;
    box-sizing: border-box;
  }

  .publish-button {
    background-color: #7C8CB1;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 15px 30px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    width: 100%;
    transition: background-color 0.2s;
  }

  .publish-button:hover {
    background-color: #6372A0;
  }

  /* Remove the modal overlay styles since we're not using it anymore */
  .modal-overlay {
    display: none;
  }

  /* Add these CSS rules to your existing styles */
  .topic-icon.active {
    border: 2px solid #3498db;
    background-color: rgba(52, 152, 219, 0.1);
  }
  
  .loading, .error, .no-posts {
    padding: 20px;
    text-align: center;
    margin: 20px 0;
    border-radius: 8px;
  }
  
  .loading {
    background-color: #f8f9fa;
  }
  
  .error {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .no-posts {
    background-color: #e9ecef;
    color: #495057;
  }
  
  .post-text {
    margin: 10px 0;
    line-height: 1.5;
  }
  
  .comment-date {
    font-size: 0.8rem;
    color: #6c757d;
    margin-top: 5px;
  }
  
  .no-comments {
    text-align: center;
    padding: 10px;
    color: #6c757d;
  }
  
  .add-comment-form {
    margin-top: 20px;
    border-top: 1px solid #e9ecef;
    padding-top: 15px;
  }
  
  .add-comment-form textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    margin-bottom: 10px;
    min-height: 60px;
  }
  
  .add-comment-form button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .add-comment-form button:hover {
    background-color: #2980b9;
  }
  
  .post-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
  }
  
  .meta-item.author {
    display: flex;
    align-items: center;
    margin-right: 15px;
  }
  
  .meta-item.likes {
    cursor: pointer;
  }
  
  .file-upload {
    position: relative;
    display: inline-block;
    width: 100%;
  }
  
  .file-upload input[type="file"] {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
    width: 0.1px;
    height: 0.1px;
    overflow: hidden;
  }
  
  .file-upload-label {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 10px;
    background-color: #f8f9fa;
    border: 1px dashed #ced4da;
    border-radius: 4px;
    cursor: pointer;
    min-height: 100px;
  }
  
  .file-upload-label:hover {
    background-color: #e9ecef;
  }

  /* Add these CSS rules to your existing styles */
  .auth-error {
    background-color: #f8d7da;
    color: #721c24;
    padding: 10px 15px;
    border-radius: 5px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .login-link {
    color: #0066cc;
    text-decoration: underline;
    font-weight: bold;
    margin-left: 10px;
  }
</style>
