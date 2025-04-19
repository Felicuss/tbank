<script lang="ts">
  import ChatBot from '$lib/components/ChatBot.svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import Profile from '$lib/components/Profile.svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { authStore } from '$lib/services/auth';
  import { browser } from '$app/environment';
  
  $: isAuthPage = $page.url.pathname === '/login' || $page.url.pathname === '/register';

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

<div class="app-container">
  {#if !isAuthPage}
    <Navbar />
    <Profile />
    <ChatBot />
  {/if}
  <main>
    <slot />
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

  .app-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0;
    box-sizing: border-box;
    position: relative;
  }
  
  main {
    width: 100%;
    min-height: calc(100vh - 40px);
    box-sizing: border-box;
  }

  @media (max-width: 768px) {
    .app-container {
      padding: 0;
    }
  }
</style> 