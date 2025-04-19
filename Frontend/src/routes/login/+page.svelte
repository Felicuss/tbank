<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/services/auth';

  let username = '';
  let password = '';
  let rememberMe = false;
  let passwordInput: HTMLInputElement;
  let errorMessage = '';
  let isLoading = false;

  async function handleLogin() {
    if (!username || !password) {
      errorMessage = 'Пожалуйста, заполните все поля';
      return;
    }

    try {
      isLoading = true;
      errorMessage = '';
      
      const success = await authStore.login({ username, password });
      
      if (!success) {
        errorMessage = 'Неверный логин или пароль';
        return;
      }
      
      // Перенаправляем на главную страницу после успешного входа
      goto('/');
    } catch (error) {
      console.error('Ошибка при входе:', error);
      errorMessage = 'Произошла ошибка при подключении к серверу';
    } finally {
      isLoading = false;
    }
  }

  function togglePassword() {
    if (passwordInput) {
      passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    }
  }
</script>

<div class="fullscreen-container">
  <div class="page-container">
    <div class="content-wrapper">
      <div class="left-section">
        <h1>Твой ФФ</h1>
        <h2>университет в одном клике.</h2>
        <div class="phone-image">
          <img src="/phone.svg" alt="Телефон с лицом" />
        </div>
      </div>
      
      <div class="registration-modal">
        <div class="modal-header">
          <h3>Вход</h3>
          <a href="/" class="close-button">×</a>
        </div>
        
        <div class="modal-body">
          {#if errorMessage}
            <div class="error-message">
              {errorMessage}
            </div>
          {/if}
          
          <div class="form-group">
            <label for="username">Логин</label>
            <input 
              type="text" 
              id="username" 
              bind:value={username} 
              placeholder="Введите логин" 
              required
            />
          </div>
          
          <div class="form-group">
            <label for="password">Пароль</label>
            <div class="password-input-container">
              <input 
                type="password"
                id="password" 
                bind:value={password}
                bind:this={passwordInput}
                placeholder="Введите пароль" 
                required
              />
              <button class="toggle-password" on:click={togglePassword}>
                <img src="/showoff.svg" alt="Toggle password" />
              </button>
            </div>
          </div>

          <div class="additional-options">
            <label class="remember-me">
              <input 
                type="checkbox" 
                bind:checked={rememberMe}
              />
              <span>Запомнить меня</span>
            </label>
            <a href="/forgot-password" class="forgot-password">Забыл пароль</a>
          </div>
          
          <button class="login-button" on:click={handleLogin} disabled={isLoading}>
            {isLoading ? 'Вход...' : 'Войти'}
          </button>
          
          <div class="register-link">
            <span>У вас еще нет аккаунта? <a href="/register">Зарегистрироваться</a></span>
          </div>
        </div>
      </div>
    </div>
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
    background-color: #333333;
    overflow-x: hidden;
  }

  .fullscreen-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }

  .page-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
    background-image: url('/fone1.svg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
    overflow: hidden;
    box-sizing: border-box;
  }

  .content-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80%;
    max-width: 1200px;
  }

  .left-section {
    flex: 1;
    color: white;
    position: relative;
    padding-right: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 100vh;
  }

  .left-section h1 {
    font-size: 42px;
    margin: 0;
    font-weight: 550;
    color: #000000;
    margin-top: 100px;
  }

  .left-section h2 {
    font-size: 32px;
    margin: 0;
    font-weight: 550;
    color: #000000;
    margin-top: 10px;
  }

  .phone-image {
    position: relative;
    width: 100%;
    max-width: 430px;
    margin-top: auto;
    margin-left: 50px;
  }

  .phone-image img {
    width: 100%;
    height: auto;
    display: block;
  }

  .registration-modal {
    background-image: url('/panel1.svg');
    background-size: cover;
    background-position: center;
    border-radius: 10px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
    border: 0px solid rgba(0, 0, 0, 0.05);
    width: 400px;
    overflow: hidden;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
  }

  .modal-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 700;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #999;
    text-decoration: none;
  }

  .modal-body {
    padding: 20px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-size: 14px;
    color: #333;
  }

  .form-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    font-size: 14px;
    background-color: #181B22;
    color: white;
    box-sizing: border-box;
  }

  .form-group input::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  .additional-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .remember-me {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #464545;
    opacity: 1;
  }

  .forgot-password {
    font-size: 14px;
    color: #666666;
    text-decoration: none;
    opacity: 0.6;
  }

  .forgot-password:hover {
    text-decoration: underline;
    opacity: 0.8;
  }

  .login-button {
    background-color: #2F4A8D;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px;
    width: 100%;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
    margin-bottom: 15px;
  }

  .login-button:hover {
    background-color: #263c71;
  }

  .register-link {
    text-align: center;
    font-size: 14px;
    color: #666;
  }

  .register-link a {
    color: #2F4A8D;
    text-decoration: none;
    font-weight: 500;
  }

  .register-link a:hover {
    text-decoration: underline;
  }

  .password-input-container {
    position: relative;
    width: 100%;
  }

  .toggle-password {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
  }

  .toggle-password img {
    width: 20px;
    height: 20px;
    opacity: 0.5;
    filter: invert(1);
  }

  .toggle-password:hover img {
    opacity: 0.8;
  }

  .error-message {
    background-color: rgba(255, 0, 0, 0.1);
    color: #ff3333;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 15px;
    font-size: 14px;
  }

  button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
</style> 