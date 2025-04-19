<script lang="ts">
  // Активный день недели (по умолчанию - понедельник)
  let activeDay = 'Пн';
  
  // Дни недели
  const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
  
  // Данные для расписания
  interface ScheduleItem {
    time: string;
    subject: string;
    location: string;
  }
  
  // Расписание для каждого дня недели
  const schedule: Record<string, ScheduleItem[]> = {
    'Пн': [
      { time: '9.00-10.35', subject: 'Персональная эффективность', location: 'Л-811' },
      { time: '10.50-12.25', subject: 'ОО Программирование', location: 'А-520' },
      { time: '12.40-14.15', subject: 'Физкультура', location: 'Спортзал' },
      { time: '14.30-16.05', subject: 'Дискретная математика', location: 'Л-811' }
    ],
    'Вт': [
      { time: '9.00-10.35', subject: 'Английский язык', location: 'А-510' },
      { time: '10.50-12.25', subject: 'Базы данных', location: 'А-520' },
      { time: '12.40-14.15', subject: 'Операционные системы', location: 'Л-621' }
    ],
    'Ср': [
      { time: '10.50-12.25', subject: 'Архитектура компьютера', location: 'А-520' },
      { time: '12.40-14.15', subject: 'Веб-разработка', location: 'А-330' },
      { time: '14.30-16.05', subject: 'Проектная деятельность', location: 'Л-812' }
    ],
    'Чт': [
      { time: '9.00-10.35', subject: 'Математический анализ', location: 'Л-813' },
      { time: '10.50-12.25', subject: 'История', location: 'А-520' },
      { time: '12.40-14.15', subject: 'Физкультура', location: 'Спортзал' }
    ],
    'Пт': [
      { time: '9.00-10.35', subject: 'Теория вероятностей', location: 'Л-811' },
      { time: '10.50-12.25', subject: 'Экономика', location: 'А-520' },
      { time: '12.40-14.15', subject: 'Алгоритмы и структуры данных', location: 'Л-621' }
    ],
    'Сб': [
      { time: '9.00-10.35', subject: 'Факультатив', location: 'Л-811' },
      { time: '10.50-12.25', subject: 'Консультация', location: 'А-520' }
    ]
  };
  
  // Переключение активного дня
  function setActiveDay(day: string) {
    activeDay = day;
  }
</script>

<div class="schedule-page"></div>
<div class="schedule-content">
  <!-- Содержимое страницы расписания -->
  <div class="schedule-container">
    <h1 class="title">Расписание</h1>
    <p class="subtitle">Все пары в одном месте</p>
    
    <!-- Дни недели -->
    <div class="weekdays">
      {#each weekDays as day}
        <button 
          class="day-button {day === activeDay ? 'active' : ''}" 
          on:click={() => setActiveDay(day)}
        >
          {day}
        </button>
      {/each}
    </div>
    
    <!-- Таблица с расписанием -->
    <div class="schedule-table">
      {#each schedule[activeDay] as item}
        <div class="schedule-row">
          <div class="time">{item.time}</div>
          <div class="subject">{item.subject}</div>
          <div class="location">{item.location}</div>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  /* Стили для страницы и фона */
  .schedule-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('/rasp_background.png');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    z-index: -1;
  }
  
  .schedule-content {
    position: relative;
    min-height: 100vh;
    padding-bottom: 40px;
    z-index: 1;
  }
  
  /* Стили для расписания */
  .schedule-container {
    padding: 20px 0;
    max-width: 900px;
    margin: 0 auto;
  }
  
  .title {
    font-size: 32px;
    color: #333;
    margin: 0 0 5px 0;
  }
  
  .subtitle {
    font-size: 18px;
    color: #666;
    margin: 0 0 30px 0;
  }
  
  /* Дни недели */
  .weekdays {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    overflow-x: auto;
    padding-bottom: 5px;
  }
  
  .day-button {
    width: 80px;
    height: 80px;
    border-radius: 10px;
    border: none;
    background-color: white;
    color: #294380;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    flex-shrink: 0;
  }
  
  .day-button.active {
    background-color: #294380;
    color: white;
  }
  
  /* Таблица расписания */
  .schedule-table {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .schedule-row {
    display: flex;
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  }
  
  .time {
    width: 150px;
    font-weight: bold;
    color: #333;
  }
  
  .subject {
    flex: 1;
    color: #444;
  }
  
  .location {
    width: 100px;
    text-align: right;
    color: #666;
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .weekdays {
      flex-wrap: wrap;
      justify-content: center;
    }
    
    .schedule-row {
      flex-direction: column;
      gap: 10px;
    }
    
    .time, .subject, .location {
      width: 100%;
      text-align: left;
    }
    
    .location {
      text-align: left;
    }
  }
</style>