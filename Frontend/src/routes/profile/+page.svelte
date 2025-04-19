<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/services/auth';
  import { goto } from '$app/navigation';
  import type { UserData } from '$lib/services/auth';
  
  let user: UserData | null = null;
  let isLoading = true;
  
  onMount(() => {
    const unsubAuth = authStore.isAuthenticated.subscribe((isAuth) => {
      if (!isAuth) {
        goto('/login');
      }
    });
    
    const unsubUser = authStore.user.subscribe((userData) => {
      user = userData;
      isLoading = false;
    });
    
    return () => {
      unsubAuth();
      unsubUser();
    };
  });
  
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
        </div>
        
        <div class="profile-actions">
          <button class="edit-button">Редактировать профиль</button>
          <button class="change-password-button">Сменить пароль</button>
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
    cursor: pointer;
    transition: all 0.2s;
    border: none;
  }
  
  .edit-button {
    background-color: #007aff;
    color: white;
    flex: 1;
  }
  
  .edit-button:hover {
    background-color: #0056b3;
  }
  
  .change-password-button {
    background-color: #f0f0f0;
    color: #333;
  }
  
  .change-password-button:hover {
    background-color: #e0e0e0;
  }
  
  @media (max-width: 768px) {
    .profile-header {
      flex-direction: column;
      text-align: center;
    }
    
    .avatar-container {
      margin-right: 0;
      margin-bottom: 20px;
    }
    
    .profile-actions {
      flex-direction: column;
    }
  }
</style> 