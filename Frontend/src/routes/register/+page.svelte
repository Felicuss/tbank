<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/services/auth';

  let firstName = '';
  let lastName = '';
  let username = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let passwordInput: HTMLInputElement;
  let confirmPasswordInput: HTMLInputElement;
  let errorMessage = '';
  let isLoading = false;

  async function handleRegister() {
    if (password !== confirmPassword) {
      errorMessage = 'Пароли не совпадают';
      return;
    }

    if (!firstName || !lastName || !username || !email || !password) {
      errorMessage = 'Пожалуйста, заполните все поля';
      return;
    }

    try {
      isLoading = true;
      errorMessage = '';
      
      const success = await authStore.register({
        first_name: firstName,
        last_name: lastName,
        username: username,
        email: email,
        password: password,
        role: 'student', // По умолчанию регистрируем студентов
      });
      
      if (!success) {
        errorMessage = 'Ошибка при регистрации';
        return;
      }
      
      // После успешной регистрации перенаправляем на страницу входа
      goto('/login');
    } catch (error) {
      console.error('Ошибка при регистрации:', error);
      errorMessage = 'Произошла ошибка при подключении к серверу';
    } finally {
      isLoading = false;
    }
  }

  function togglePassword(input: HTMLInputElement) {
    if (input) {
      input.type = input.type === 'password' ? 'text' : 'password';
    }
  }
</script>

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
        <h3>Регистрация</h3>
        <a href="/" class="close-button">×</a>
      </div>
      
      <div class="modal-body">
        {#if errorMessage}
          <div class="error-message">
            {errorMessage}
          </div>
        {/if}
        
        <div class="form-group">
          <label for="firstName">Имя</label>
          <input 
            type="text" 
            id="firstName" 
            bind:value={firstName} 
            placeholder="Введите ваше имя" 
            required
          />
        </div>
        
        <div class="form-group">
          <label for="lastName">Фамилия</label>
          <input 
            type="text" 
            id="lastName" 
            bind:value={lastName} 
            placeholder="Введите вашу фамилию" 
            required
          />
        </div>
        
        <div class="form-group">
          <label for="username">Логин</label>
          <input 
            type="text" 
            id="username" 
            bind:value={username} 
            placeholder="Придумайте логин" 
            required
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            bind:value={email} 
            placeholder="Введите ваш email" 
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
              placeholder="Придумайте пароль" 
              required
            />
            <button class="toggle-password" on:click={() => togglePassword(passwordInput)}>
              <img src="/showoff.svg" alt="Toggle password" />
            </button>
          </div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Повторите пароль</label>
          <div class="password-input-container">
            <input 
              type="password" 
              id="confirmPassword" 
              bind:value={confirmPassword} 
              bind:this={confirmPasswordInput}
              placeholder="Введите пароль" 
              required
            />
            <button class="toggle-password" on:click={() => togglePassword(confirmPasswordInput)}>
              <img src="/showoff.svg" alt="Toggle password" />
            </button>
          </div>
        </div>
        
        <button class="register-button" on:click={handleRegister} disabled={isLoading}>
          {isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
        </button>
        
        <div class="login-link">
          <span>Уже есть аккаунт? <a href="/login">Войти</a></span>
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

  .page-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    min-height: 100vh;
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
    overflow-x: hidden;
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
    border: 0.5px solid rgba(0, 0, 0, 0.05);
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

  .register-button {
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

  .register-button:hover {
    background-color: #263c71;
  }

  .login-link {
    text-align: center;
    font-size: 14px;
    color: #666;
  }

  .login-link a {
    color: #2F4A8D;
    text-decoration: none;
    font-weight: 500;
  }

  .login-link a:hover {
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