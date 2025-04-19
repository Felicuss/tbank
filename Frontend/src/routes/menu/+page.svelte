<script lang="ts">
  import { onMount } from 'svelte';
  
  interface MenuItem {
    id: number;
    title: string;
    image: string;
    description?: string;
    date?: string;
  }
  
  interface Product {
    name: string;
    image: string;
    calories: string;
    nutrients: string;
  }
  
  interface DayMenu {
    day: string;
    dayName: string;
    products: Product[];
    selectedProductIndex: number;
  }
  
  // Хиты недели
  let weeklyHits: MenuItem[] = [
    {
      id: 1,
      title: 'ПРОТ',
      image: '/menu1.png',
      description: 'ПРОТЕИНОВЫЙ БАТОНЧИК БЕЗ САХАРА СИНКАБАР'
    },
    {
      id: 2,
      title: 'SUSHI',
      image: '/menu2.png',
      description: 'BORA BORA'
    },
    {
      id: 3,
      title: 'БЛИНЫ',
      image: '/menu3.png',
      description: 'SO DELICIOUS!',
      date: '12-18 МАРТА'
    }
  ];
  
  // Дневное меню
  let daysMenu: DayMenu[] = [
    {
      day: 'Пн',
      dayName: 'День 1',
      selectedProductIndex: 0,
      products: [
        { 
          name: 'Пицца', 
          image: '/menu1(1).png',
          calories: 'Калории: 220 ккал.',
          nutrients: 'Белки: 12.5 гр. Жиры: 9.8 гр. Углеводы: 22.3 гр.'
        },
        { 
          name: 'Капучино', 
          image: '/menu1(2).png',
          calories: 'Калории: 120 ккал.',
          nutrients: 'Белки: 6.2 гр. Жиры: 4.8 гр. Углеводы: 12.5 гр.'
        },
        { 
          name: 'Цезарь', 
          image: '/menu1(3).png',
          calories: 'Калории: 179.6 ккал.',
          nutrients: 'Белки: 14.3 гр. Жиры: 8.6 гр. Углеводы: 10.8 гр.'
        }
      ]
    },
    {
      day: 'Вт',
      dayName: 'День 2',
      selectedProductIndex: 0,
      products: [
        { 
          name: 'Чай', 
          image: '/menu1(1).png',
          calories: 'Калории: 3 ккал.',
          nutrients: 'Белки: 0 гр. Жиры: 0 гр. Углеводы: 0.9 гр.'
        },
        { 
          name: 'Рис', 
          image: '/menu1(2).png',
          calories: 'Калории: 130 ккал.',
          nutrients: 'Белки: 2.7 гр. Жиры: 0.3 гр. Углеводы: 28.2 гр.'
        },
        { 
          name: 'Том ям', 
          image: '/menu1(3).png',
          calories: 'Калории: 95 ккал.',
          nutrients: 'Белки: 7.8 гр. Жиры: 4.2 гр. Углеводы: 8.1 гр.'
        }
      ]
    },
    {
      day: 'Ср',
      dayName: 'День 3',
      selectedProductIndex: 0,
      products: [
        { 
          name: 'Борщ', 
          image: '/menu1(1).png',
          calories: 'Калории: 85 ккал.',
          nutrients: 'Белки: 4.8 гр. Жиры: 3.2 гр. Углеводы: 9.5 гр.'
        },
        { 
          name: 'Курица', 
          image: '/menu1(2).png',
          calories: 'Калории: 285 ккал.',
          nutrients: 'Белки: 10.6 гр. Жиры: 2.3 гр. Углеводы: 56.7 гр.'
        },
        { 
          name: 'Салат', 
          image: '/menu1(3).png',
          calories: 'Калории: 145 ккал.',
          nutrients: 'Белки: 3.5 гр. Жиры: 12.1 гр. Углеводы: 6.2 гр.'
        }
      ]
    }
  ];
  
  // Функция выбора продукта
  function selectProduct(dayIndex: number, productIndex: number) {
    daysMenu[dayIndex].selectedProductIndex = productIndex;
  }
  
  let currentHitIndex = 0;
  
  function prevHit() {
    if (currentHitIndex > 0) {
      currentHitIndex--;
    } else {
      currentHitIndex = weeklyHits.length - 1;
    }
  }
  
  function nextHit() {
    if (currentHitIndex < weeklyHits.length - 1) {
      currentHitIndex++;
    } else {
      currentHitIndex = 0;
    }
  }
  
  onMount(() => {
    // Автоматическое пролистывание карусели каждые 5 секунд
    const interval = setInterval(() => {
      nextHit();
    }, 5000);
    
    return () => {
      clearInterval(interval);
    };
  });
</script>

<div class="container">
  <h1 class="menu-title">Меню столовой</h1>

  <!-- Хиты недели -->
  <div class="hits-section">
    <h2 class="section-title">
      Хиты недели <span class="lightning-icon">⚡</span>
    </h2>
    
    <div class="hits-grid">
      {#each weeklyHits as hit}
        <div class="hit-card">
          <img src={hit.image} alt={hit.title} class="hit-image">
        </div>
      {/each}
    </div>
  </div>

  <!-- Дневное меню -->
  <div class="daily-menu">
    {#each daysMenu as day, dayIndex}
      <div class="day-card">
        <div class="day-info">
          <div class="calendar-icon">
            <span class="day-name">{day.day}</span>
          </div>
          <div class="meal-info">
            <h3 class="dish-title">{day.dayName}</h3>
            <p class="calories-info">{day.products[day.selectedProductIndex].calories}</p>
            <p class="details">{day.products[day.selectedProductIndex].nutrients}</p>
          </div>
        </div>
        
        <div class="products-row">
          {#each day.products as product, productIndex}
            <div 
              class="product-item" 
              class:selected={productIndex === day.selectedProductIndex}
              on:click={() => selectProduct(dayIndex, productIndex)}
            >
              <img src={product.image} alt={product.name} class="product-image">
              <span class="product-name">{product.name}</span>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  /* Контейнер */
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Основные стили для страницы меню */
  .menu-title {
    font-size: 32px;
    margin: 20px 0;
    color: #333;
    text-align: center;
  }
  
  /* Стили для раздела "Хиты недели" */
  .hits-section {
    margin: 30px 0;
  }
  
  .section-title {
    font-size: 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .lightning-icon {
    color: #FFD700;
    font-size: 20px;
  }
  
  /* Стили для грида хитов */
  .hits-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-bottom: 30px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .hit-card {
    aspect-ratio: auto;
    background-color: transparent;
    border-radius: 0;
    overflow: visible;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    max-width: 280px;
    margin: 0 auto;
  }
  
  .hit-image {
    width: 100%;
    height: auto;
    object-fit: contain;
    max-height: 280px;
  }
  
  /* Стили для дневного меню */
  .daily-menu {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 40px;
  }
  
  .day-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f2f2f2;
    border-radius: 15px;
    padding: 15px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .day-info {
    display: flex;
    align-items: center;
    gap: 20px;
  }
  
  .calendar-icon {
    width: 60px;
    height: 60px;
    background-color: #333;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }
  
  .calendar-icon:before {
    display: none;
  }
  
  .calendar-icon:after {
    display: none;
  }
  
  .day-name {
    font-size: 24px;
    font-weight: bold;
    color: white;
  }
  
  .meal-info {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  .dish-title {
    font-size: 24px;
    margin: 0;
    font-weight: bold;
  }
  
  .calories-info {
    margin: 0;
    color: #555;
    font-size: 14px;
  }
  
  .details {
    font-size: 14px;
    color: #666;
    margin: 0;
  }
  
  .products-row {
    display: flex;
    gap: 20px;
    justify-content: flex-end;
  }
  
  .product-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    padding: 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    width: 110px;
    height: 110px;
    position: relative;
  }
  
  .product-image {
    width: 85px;
    height: 85px;
    object-fit: contain;
    border-radius: 0;
  }
  
  .product-name {
    font-size: 14px;
    text-align: center;
    position: absolute;
    bottom: 5px;
    max-width: 90%;
  }
  
  .product-item.selected {
    background-color: #465E44;
  }
  
  .product-item.selected .product-name {
    color: white;
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .hits-grid {
      grid-template-columns: 1fr;
    }
    
    .hit-card {
      height: 200px;
    }
    
    .day-card {
      flex-direction: column;
      align-items: flex-start;
      gap: 15px;
    }
    
    .products-row {
      width: 100%;
      justify-content: space-between;
    }
  }
</style>