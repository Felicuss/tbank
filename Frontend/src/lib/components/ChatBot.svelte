<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '$lib/services/auth';
  import { 
    chatHistoryStore, 
    isLoadingStore, 
    loadChatHistory, 
    sendMessage, 
    clearChatHistory,
    getHints
  } from '$lib/services/assistant';
  import { page } from '$app/stores';
  import { marked } from 'marked';
  import DOMPurify from 'dompurify';
  
  let showChatBubble = true;
  let showChatDialog = false;
  let userMessage = '';
  let isLoading = false;
  let currentContext = '';
  let isAuthenticated = false;
  
  // Subscribe to the loading state
  isLoadingStore.subscribe(value => {
    isLoading = value;
  });
  
  // Subscribe to the authentication state
  authStore.isAuthenticated.subscribe(value => {
    isAuthenticated = value;
  });
  
  function closeChatBubble() {
    showChatBubble = false;
  }
  
  function toggleChatDialog() {
    showChatDialog = !showChatDialog;
    showChatBubble = false;
    
    if (showChatDialog) {
      loadChatHistory();
    }
  }
  
  function closeChatDialog() {
    showChatDialog = false;
  }
  
  async function handleSendMessage() {
    if (userMessage.trim() !== '') {
      currentContext = $page.url.pathname;
      await sendMessage(userMessage, currentContext);
      userMessage = '';
    }
  }
  
  function handleClearHistory() {
    clearChatHistory();
  }
  
  function getCurrentDate() {
    const now = new Date();
    const months = [
      'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
      'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ];
    return `${now.getDate()} ${months[now.getMonth()]}`;
  }
  
  // Функция для преобразования текста в HTML с поддержкой маркдауна
  function formatMessageContent(content: string, isBotMessage: boolean) {
    if (!isBotMessage) return content; // Для сообщений пользователя просто возвращаем текст
    
    // Настраиваем marked для распознавания ссылок и других элементов маркдауна
    marked.setOptions({
      breaks: true, // Переносы строк как <br>
      gfm: true, // GitHub Flavored Markdown
    });
    
    // Преобразуем маркдаун в HTML
    const html = marked.parse(content);
    
    // Очищаем HTML от потенциально опасных элементов
    const cleanHtml = DOMPurify.sanitize(html, {
      ADD_ATTR: ['target', 'rel'], // Разрешаем атрибуты target и rel для ссылок
      ADD_TAGS: ['iframe'], // Разрешаем iframe, если нужно
    });
    
    return cleanHtml;
  }
  
  onMount(() => {
    // Check if current page has hints
    currentContext = $page.url.pathname;
    getHints(currentContext).then(hints => {
      if (hints.length > 0) {
        showChatBubble = true;
      }
    });
  });
</script>

{#if isAuthenticated}
  <div class="chat-bot">
    {#if showChatBubble}
      <div class="chat-bubble">
        <span class="close-bubble" on:click={closeChatBubble}>&times;</span>
        Привет! Я - физик,<br>твой виртуальный помощник
      </div>
    {/if}
    <div class="bot-icon" on:click={toggleChatDialog}>
      <img src="/chatbot head.png" alt="Чат-бот" />
    </div>
  </div>

  {#if showChatDialog}
    <div class="chat-dialog-overlay">
      <div class="chat-dialog">
        <div class="chat-header">
          <div class="chat-header-left">
            <img src="/chatbot head.png" alt="Физик" class="chat-avatar" />
            <h3>Физик чат-бот</h3>
          </div>
          <div class="chat-header-right">
            <button class="settings-button" on:click={handleClearHistory}>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18"></path>
                <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"></path>
              </svg>
            </button>
            <button class="close-dialog" on:click={closeChatDialog}>&times;</button>
          </div>
        </div>
        
        <div class="chat-divider"></div>
        
        <div class="chat-date">
          {getCurrentDate()}
        </div>
        
        <div class="chat-messages">
          {#if $chatHistoryStore.length === 0}
            <div class="message bot">
              <div class="message-sender">Физик</div>
              <div class="message-content">
                Привет! Я - физик,<br>
                твой виртуальный помощник<br>
                С чем тебе помочь сегодня?<br>
                Навигация по сайту или<br>
                пересказ лекции?
              </div>
            </div>
          {:else}
            {#each $chatHistoryStore as message}
              <div class="message {message.sender === 'Assistant' ? 'bot' : 'user'}">
                <div class="message-sender">{message.sender === 'Assistant' ? 'Физик' : 'Вы'}</div>
                <div class="message-content">
                  {#if message.sender === 'Assistant'}
                    {@html formatMessageContent(message.content, true)}
                  {:else}
                    {message.content}
                  {/if}
                </div>
              </div>
            {/each}
          {/if}
        </div>
        
        <div class="chat-input">
          <button class="voice-button" disabled={isLoading}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
          </button>
          <input 
            type="text" 
            placeholder="Ваше сообщение" 
            bind:value={userMessage}
            on:keydown={(e) => e.key === 'Enter' && handleSendMessage()}
            disabled={isLoading}
          />
          <button class="send-button" on:click={handleSendMessage} disabled={isLoading}>
            {#if isLoading}
              <svg class="spinner" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" />
              </svg>
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            {/if}
          </button>
        </div>
      </div>
    </div>
  {/if}
{/if}

<style>
  /* Chat Bot */
  .chat-bot {
    position: fixed;
    bottom: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 15px;
  }

  .chat-bot img {
    width: 65px;
    height: 65px;
    cursor: pointer;
  }

  .chat-bubble {
    position: absolute;
    bottom: 70px;
    right: 20px;
    background-color: #fff;
    padding: 10px 20px;
    border-radius: 18px;
    width: 320px;
    max-width: 90vw;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    font-size: 14px;
    line-height: 1.4;
    z-index: 10;
    border: 1px solid #e0e0e0;
    text-align: left;
  }

  .close-bubble {
    position: absolute;
    top: 5px;
    right: 12px;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    color: #aaa;
    line-height: 1;
  }

  .close-bubble:hover {
    color: #555;
  }

  .chat-bubble:after {
    content: '';
    position: absolute;
    bottom: -10px;
    right: 20px;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 10px solid #fff;
  }
  
  /* Chat Dialog */
  .chat-dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 3000;
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
  }
  
  .chat-dialog {
    width: 90%;
    max-width: 450px;
    height: 80vh;
    background-color: #f5f5f5;
    border-radius: 20px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    margin-right: 10px;
    margin-bottom: 10px;
  }
  
  .chat-header {
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ffffff;
  }
  
  .chat-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .chat-header-left h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
  }
  
  .chat-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  
  .chat-header-right {
    display: flex;
    align-items: center;
    gap: 15px;
  }
  
  .settings-button, .close-dialog {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #555;
  }
  
  .close-dialog {
    font-size: 24px;
    font-weight: bold;
    color: #999;
  }
  
  .chat-divider {
    height: 1px;
    background-color: #e0e0e0;
    width: 100%;
  }
  
  .chat-date {
    text-align: center;
    padding: 15px 0;
    color: #999;
    font-size: 16px;
  }
  
  .chat-messages {
    flex: 1;
    padding: 0 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .message {
    max-width: 70%;
    border-radius: 18px;
    padding: 12px 15px;
    position: relative;
  }
  
  .message.bot {
    align-self: flex-start;
    background-color: #fff;
    border-top-left-radius: 0;
  }
  
  .message.user {
    align-self: flex-end;
    background-color: #e3f2fd;
    border-top-right-radius: 0;
  }
  
  .message-sender {
    font-weight: 600;
    margin-bottom: 5px;
    font-size: 14px;
  }
  
  .message-content {
    line-height: 1.4;
  }
  
  /* Стили для элементов маркдауна */
  :global(.message-content a) {
    color: #1a73e8;
    text-decoration: none;
    border-bottom: 1px dashed #1a73e8;
    transition: all 0.2s ease;
  }
  
  :global(.message-content a:hover) {
    color: #0d47a1;
    border-bottom: 1px solid #0d47a1;
  }
  
  :global(.message-content p) {
    margin: 0 0 8px 0;
  }
  
  :global(.message-content p:last-child) {
    margin-bottom: 0;
  }
  
  :global(.message-content ul, .message-content ol) {
    margin-top: 0;
    margin-bottom: 8px;
    padding-left: 20px;
  }
  
  :global(.message-content code) {
    font-family: monospace;
    background-color: #f0f0f0;
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 0.9em;
  }
  
  :global(.message-content pre) {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 10px 0;
  }
  
  :global(.message-content pre code) {
    background-color: transparent;
    padding: 0;
  }
  
  .chat-input {
    padding: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: #fff;
    border-top: 1px solid #e0e0e0;
  }
  
  .chat-input input {
    flex: 1;
    padding: 10px 15px;
    border: none;
    border-radius: 30px;
    background-color: #f0f0f0;
    font-size: 16px;
    outline: none;
  }
  
  .voice-button, .send-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: none;
    color: #999;
  }
  
  .voice-button:disabled, .send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .send-button {
    color: #666;
  }
  
  .spinner {
    animation: spin 1s linear infinite;
    stroke-dasharray: 50;
    stroke-dashoffset: 50;
  }
  
  @keyframes spin {
    0% {
      transform: rotate(0deg);
      stroke-dashoffset: 50;
    }
    50% {
      stroke-dashoffset: 0;
    }
    100% {
      transform: rotate(360deg);
      stroke-dashoffset: 50;
    }
  }

  @media (max-width: 768px) {
    .chat-dialog {
      width: 100%;
      height: 100%;
      max-width: 100%;
      border-radius: 0;
      margin-right: 0;
    }
  }

  .bot-icon {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    z-index: 1000;
    box-shadow: none;
  }
  
  .bot-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
</style> 