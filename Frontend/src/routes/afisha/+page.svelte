<script lang="ts">
  import { onMount } from 'svelte';

  let avatar = '/avatar.png';
  
  interface Event {
    id: number;
    title: string;
    description: string;
    image: string;
    tag: string;
    fullDescription: string;
  }

  let events: Event[] = [
    {
      id: 1,
      title: 'Универсиада «Ломоносов» 2025',
      description: 'МГУ приглашает студентов принять участие в Универсиаде "Ломоносов" по математическим методам в экономике. Отличная возможность для развития математических навыков.',
      image: '/event1.png',
      tag: '#Универсиада',
      fullDescription: 'Полное описание Универсиады «Ломоносов» 2025'
    },
    {
      id: 2,
      title: 'Путёвки в здравницы МГУ',
      description: 'С 20.02.2025 реализуются путёвки в здравницы МГУ на сезон 2025 года. Оформление путёвок в отделе реализации социальных программ.',
      image: '/event2.png',
      tag: '#Университетская жизнь',
      fullDescription: 'Полное описание путёвок в здравницы МГУ'
    }
  ];
  
  onMount(() => {
    // Any initialization code can go here
  });
</script>

<div class="page-container">
  <div class="container">
    <main>
      <div class="content-header">
        <h2 class="main-title">Конференции<br>и мероприятия</h2>
        
        <div class="filters">
          <div class="filter-group">
            <label>Поиск по хештегам</label>
            <select class="filter-select">
              <option>Любой</option>
              <option>Универсиада</option>
              <option>Университетская жизнь</option>
              <option>Конференция</option>
              <option>Олимпиада</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>По новизне</label>
            <select class="filter-select">
              <option>Любой</option>
              <option>Сначала новые</option>
              <option>Сначала старые</option>
            </select>
          </div>
        </div>
      </div>

      <div class="events-list">
        {#each events as event}
          <div class="event-card">
            <div class="event-image">
              <img src={event.image} alt={event.title} />
            </div>
            <div class="event-content">
              <div class="event-tag">{event.tag}</div>
              <h3 class="event-title">{event.title}</h3>
              <p class="event-description">{event.description}</p>
              <button class="details-button">Подробнее</button>
            </div>
          </div>
        {/each}
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

  .page-container {
    width: 100%;
    background-color: #ffffff;
    min-height: 100vh;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Content Header */
  .content-header {
    margin: 40px 0;
  }

  .main-title {
    font-size: 36px;
    font-weight: 600;
    margin-bottom: 30px;
    line-height: 1.2;
  }

  /* Filters */
  .filters {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .filter-group label {
    font-size: 14px;
    color: #666;
  }

  .filter-select {
    padding: 10px 15px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    background-color: #f5f5f5;
    width: 200px;
    font-family: 'SF Pro Display', Arial, sans-serif;
    font-size: 15px;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 16px;
  }

  /* Events List */
  .events-list {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-bottom: 60px;
  }

  .event-card {
    display: flex;
    background-color: #E4E4E4;
    border-radius: 20px;
    overflow: hidden;
  }

  .event-image {
    width: 270px;
    height: 270px;
    flex-shrink: 0;
    overflow: hidden;
    padding: 8px 0 8px 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
  }

  .event-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    max-width: 210px;
    max-height: 210px;
  }

  .event-content {
    flex: 1;
    padding: 30px;
    position: relative;
    min-height: 210px;
    display: flex;
    flex-direction: column;
  }

  .event-tag {
    display: inline-block;
    background-color: #1A3882;
    color: white;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 12px;
    margin-bottom: 15px;
    align-self: flex-start;
  }

  .event-title {
    font-size: 24px;
    font-weight: 600;
    margin: 0 0 15px 0;
    line-height: 1.3;
  }

  .event-description {
    color: #444;
    line-height: 1.5;
    margin-bottom: 20px;
    flex-grow: 1;
  }

  .details-button {
    background-color: #1A3882;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 25px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    align-self: flex-end;
    margin-top: auto;
  }

  .details-button:hover {
    background-color: #132a62;
  }

  @media (max-width: 768px) {
    .event-card {
      flex-direction: column;
    }

    .event-image {
      width: 100%;
      height: auto;
      aspect-ratio: 1/1;
      padding: 30px;
    }
    
    .event-image img {
      max-width: 100%;
      max-height: 100%;
    }
    
    .filters {
      flex-direction: column;
      gap: 15px;
    }
    
    .filter-select {
      width: 100%;
    }
    
    .event-content {
      padding: 20px;
    }
    
    .main-title {
      font-size: 28px;
    }
    
    .event-title {
      font-size: 20px;
    }
  }
</style> 