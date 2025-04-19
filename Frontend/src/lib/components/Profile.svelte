<script>
  import { authStore } from '$lib/services/auth';
  import { onMount } from 'svelte';
  
  export let avatar = '/avatar.png';
  let isMenuOpen = false;
  let user = null;
  
  onMount(() => {
    // Подписываемся на изменения в хранилище пользователя
    const unsubscribe = authStore.user.subscribe(value => {
      user = value;
      if (user && user.avatar) {
        avatar = user.avatar;
      }
    });
    
    return unsubscribe;
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
  <div class="avatar" style="background-image: url({avatar})" on:click={toggleMenu}></div>
  
  {#if isMenuOpen}
    <div class="menu">
      {#if user}
        <div class="user-info">
          <span class="username">{user.first_name} {user.last_name}</span>
          <span class="email">{user.email}</span>
        </div>
      {/if}
      <ul>
        <li><a href="/profile">Мой профиль</a></li>
        <li><button on:click={handleLogout}>Выйти</button></li>
      </ul>
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
    background-color: #ccc;
    background-size: cover;
    background-position: center;
    cursor: pointer;
  }
  
  .menu {
    position: absolute;
    top: 60px;
    right: 0;
    width: 200px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    padding: 10px 0;
    z-index: 101;
  }
  
  .user-info {
    padding: 10px 15px;
    border-bottom: 1px solid #eee;
  }
  
  .username {
    display: block;
    font-weight: 500;
    font-size: 14px;
    margin-bottom: 2px;
  }
  
  .email {
    display: block;
    font-size: 12px;
    color: #666;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  li {
    padding: 0;
  }
  
  li a, li button {
    display: block;
    padding: 8px 15px;
    text-decoration: none;
    color: #333;
    font-size: 14px;
    text-align: left;
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
  }
  
  li a:hover, li button:hover {
    background-color: #f5f5f5;
  }
  
  li button {
    color: #f44336;
  }
</style>