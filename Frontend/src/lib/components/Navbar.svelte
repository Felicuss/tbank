<script lang="ts">
  import { page } from '$app/stores';
  
  $: currentRoute = $page.url.pathname;
</script>

<nav class="navbar">
  <div class="nav-buttons">
    <a href="/schedule" class="nav-link">
      <button class="nav-button {currentRoute === '/schedule' ? 'active' : ''}">
        Расписание <span class="icon"><img src="/top1.svg" alt="Расписание"></span>
      </button>
    </a>
    <a href="/forum" class="nav-link">
      <button class="nav-button {currentRoute === '/forum' ? 'active' : ''}">
        Форум <span class="icon"><img src="/top2.svg" alt="Форум"></span>
      </button>
    </a>
    <a href="/" class="nav-link">
      <button class="nav-button {currentRoute === '/' ? 'active' : ''}">
        Сервисы <span class="icon"><img src="/top3.svg" alt="Сервисы"></span>
      </button>
    </a>
    <a href="https://t.me/" target="_blank" class="tg-link">
      <img src="/tg_icon.svg" alt="Telegram" class="tg-icon">
    </a>
  </div>
</nav>

<style>
  /* Navbar */
  .navbar {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
    margin: 0;
    padding-top: 10px;
    width: 100%;
  }

  .nav-buttons {
    display: flex;
    gap: 15px;
    align-items: center;
    margin: 0;
    padding: 0;
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
    transition: background-color 0.2s;
    margin: 0;
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
    margin: 0;
    padding: 0;
  }

  .tg-link {
    text-decoration: none;
    display: flex;
    align-items: center;
    margin: 0;
    padding: 0;
  }

  .tg-icon {
    width: 32px;
    height: 32px;
    cursor: pointer;
  }

  .nav-button.active {
    background-color: #d0d0d0;
  }

  @media (max-width: 768px) {
    .nav-buttons {
      gap: 10px;
    }
    
    .nav-button {
      font-size: 14px;
      padding: 6px 12px;
    }
    
    .icon img {
      width: 16px;
      height: 16px;
    }
    
    .tg-icon {
      width: 26px;
      height: 26px;
    }
  }
</style> 