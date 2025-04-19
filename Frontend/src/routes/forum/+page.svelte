<script lang="ts">
  import { onMount } from 'svelte';

  interface Comment {
    author: string;
    text: string;
  }
  
  interface Post {
    id: number;
    title: string;
    date: string;
    views: number;
    replies: number;
    comments: Comment[];
  }
  
  let avatar = '/avatar.png';
  
  let posts: Post[] = [
    {
      id: 1,
      title: "Лежала на диване в Б корпусе, чья?",
      date: "20 мая",
      views: 120,
      replies: 2,
      comments: [
        {
          author: "Иванов Иван",
          text: "Мне кажется, я знаю чья это тетрадка, могу передать, если нужно, что скажешь?"
        },
        {
          author: "Анонимный пользователь",
          text: "Не помню ни у кого такой"
        }
      ]
    },
    {
      id: 2,
      title: "Чей кейс от наушников? Т корпус",
      date: "",
      views: 20,
      replies: 1,
      comments: []
    }
  ];
  
  let selectedPost: Post | null = null;
  
  function viewPost(post: Post): void {
    selectedPost = selectedPost?.id === post.id ? null : post;
  }
  
  onMount(() => {
    // Any initialization code can go here
  });
</script>

<div class="container">
  <main>
    <div class="forum-header">
      <h1>Студенческий форум</h1>
      <p>5000 участников</p>
    </div>

    <div class="content">
      <div class="left-panel">
        <div class="section-header">
          <span class="section-icon"><img src="/3lines.svg" alt="Menu" /></span>
          <h2>Статьи</h2>
        </div>

        <div class="posts">
          {#each posts as post}
            <!-- Expanded view for selected post -->
            {#if selectedPost && selectedPost.id === post.id}
              <div class="post selected-post">
                <div class="user-avatar"></div>
                <div class="post-content">
                  <div class="post-image-container">
                    <div class="post-image-placeholder"></div>
                  </div>
                  <h3 class="post-title">{post.title}</h3>
                  <div class="post-meta">
                    <span class="meta-item date">
                      <img src="/mdi_calendar.svg" alt="Дата" /> {post.date}
                    </span>
                    <span class="meta-item views">
                      <img src="/viev.svg" alt="Просмотры" /> {post.views}
                    </span>
                    <span class="meta-item replies">
                      <img src="/otvet.svg" alt="Ответы" /> {post.replies} {post.replies === 1 ? 'ответ' : 'ответа'}
                    </span>
                  </div>
                  
                  <button class="view-replies collapse" on:click={() => viewPost(post)}>Свернуть ответы</button>
                  
                  <!-- Comments -->
                  <div class="post-comments">
                    {#each post.comments as comment}
                      <div class="comment">
                        <div class="user-avatar"></div>
                        <div class="comment-content">
                          <h4 class="comment-author">{comment.author}</h4>
                          <p class="comment-text">{comment.text}</p>
                        </div>
                      </div>
                    {/each}
                  </div>
                </div>
              </div>
            {:else}
              <!-- Collapsed view for other posts -->
              <div class="post">
                <div class="user-avatar"></div>
                <div class="post-content">
                  <div class="post-image-container">
                    <div class="post-image-placeholder"></div>
                  </div>
                  <h3 class="post-title">{post.title}</h3>
                  <div class="post-meta">
                    <span class="meta-item date">
                      <img src="/mdi_calendar.svg" alt="Дата" /> {post.date}
                    </span>
                    <span class="meta-item views">
                      <img src="/viev.svg" alt="Просмотры" /> {post.views}
                    </span>
                    <span class="meta-item replies">
                      <img src="/otvet.svg" alt="Ответы" /> {post.replies} {post.replies === 1 ? 'ответ' : 'ответа'}
                    </span>
                  </div>
                  <button class="view-replies" on:click={() => viewPost(post)}>Смотреть ответы</button>
                </div>
              </div>
            {/if}
          {/each}
        </div>
      </div>

      <div class="right-panel">
        <div class="about-forum">
          <div class="section-header">
            <span class="section-icon"><img src="/3lines.svg" alt="Menu" /></span>
            <h2>О форуме</h2>
          </div>
          
          <div class="info-block">
            <span class="info-icon">
              <img src="/info.svg" alt="Информация" />
            </span>
            <p>Добро пожаловать на Студенческий Хаб — место, где встречаются знания, опыт и студенческая жизнь!</p>
          </div>
          
          <p class="about-text">
            Неважно, первокурсник ты или выпускник – здесь каждый найдёт что-то полезное (и забавное).
            Присоединяйся, задавай вопросы, делись опытом и делай студенческие годы ярче!
          </p>
        </div>

        <div class="topics">
          <div class="section-header">
            <span class="section-icon"><img src="/3lines.svg" alt="Menu" /></span>
            <h2>Темы</h2>
          </div>
          
          <div class="topic-icons">
            <div class="topic">
              <div class="topic-icon">
                <img src="/cute house.png" alt="Флудилка" class="icon-house" />
              </div>
              <span>Флудилка</span>
            </div>
            <div class="topic">
              <div class="topic-icon">
                <img src="/search cute blue icon.png" alt="Потеряшки" class="icon-search" />
              </div>
              <span>Потеряшки</span>
            </div>
            <div class="topic">
              <div class="topic-icon">
                <img src="/blue speech bubble.png" alt="Подслушано" class="icon-speech" />
              </div>
              <span>Подслушано</span>
            </div>
            <div class="topic">
              <div class="topic-icon">
                <img src="/cute books.png" alt="Конспекты" class="icon-books" />
              </div>
              <span>Конспекты</span>
            </div>
            <div class="topic">
              <div class="topic-icon">
                <img src="/thumbs up.png" alt="Полезное" class="icon-thumbs" />
              </div>
              <span>Полезное</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
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

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
  }

  /* Navbar */
  .navbar {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0;
  }

  .nav-buttons {
    display: flex;
    gap: 15px;
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

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #333;
  }

  .profile {
    position: fixed;
    top: 20px;
    right: 20px;
  }

  /* Forum Header */
  .forum-header {
    margin: 40px 0;
    text-align: center;
  }

  .forum-header h1 {
    font-size: 32px;
    margin-bottom: 10px;
  }

  .forum-header p {
    color: #666;
    margin: 0;
  }

  /* Content Layout */
  .content {
    display: flex;
    gap: 20px;
  }

  .left-panel {
    flex: 1.5;
    background-color: #e6e6e6;
    border-radius: 15px;
    padding: 20px;
  }

  .right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .about-forum, .topics {
    background-color: #e6e6e6;
    border-radius: 15px;
    padding: 15px;
  }

  /* Topics */
  .topics {
    padding: 15px;
  }

  /* Section Headers */
  .left-panel .section-header,
  .about-forum .section-header,
  .topics .section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
    background-color: #1A3882;
    padding: 6px 12px;
    border-radius: 10px;
    width: fit-content;
  }

  .left-panel .section-header h2,
  .left-panel .section-header .section-icon,
  .about-forum .section-header h2,
  .about-forum .section-header .section-icon,
  .topics .section-header h2,
  .topics .section-header .section-icon {
    color: #fff;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    background-color: #c0c0c0;
    padding: 8px 15px;
    border-radius: 12px;
    width: fit-content;
  }

  .section-icon {
    display: flex;
    align-items: center;
  }

  .section-icon img {
    width: 18px;
    height: 18px;
  }

  .section-header h2 {
    font-size: 16px;
    margin: 0;
    font-weight: normal;
  }

  /* Posts */
  .posts {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .post {
    display: flex;
    gap: 8px;
  }
  
  .selected-post {
    cursor: default;
  }

  .user-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #ffffff;
    flex-shrink: 0;
    margin-top: 5px;
  }

  .post-content {
    flex: 1;
    position: relative;
    padding-left: 5px;
  }

  .post-image-container {
    display: flex;
    justify-content: flex-start;
    width: 100%;
  }

  .post-image-placeholder {
    width: 70%;
    height: 150px;
    background-color: #ffffff;
    border-radius: 10px;
    margin-bottom: 15px;
  }

  .post-title {
    font-size: 18px;
    margin: 0 0 15px 0;
    font-weight: normal;
    text-align: left;
  }

  .post-meta {
    display: flex;
    gap: 15px;
    margin-bottom: 15px;
    color: #888;
    font-size: 14px;
    align-items: center;
  }
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .meta-item img {
    width: 18px;
    height: 18px;
  }

  .view-replies {
    background-color: #1A3882;
    border: none;
    border-radius: 12px;
    padding: 8px 0;
    width: 45%;
    cursor: pointer;
    font-size: 14px;
    color: #fff;
    text-align: center;
    margin-left: 10%;
  }

  /* Topics */
  .topic-icons {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    gap: 10px;
  }

  .topic {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }

  .topic-icon {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #c0c0c0;
  }

  .topic-icon img {
    max-width: 100%;
    max-height: 100%;
  }

  /* Custom icon sizes with higher specificity */
  .topic-icon .icon-house {
    width: 48px !important;
    height: 38px !important;
  }

  .topic-icon .icon-search {
    width: 38px !important;
    height: 37px !important;
  }

  .topic-icon .icon-speech {
    width: 41px !important;
    height: 57px !important;
  }

  .topic-icon .icon-books {
    width: 40px !important;
    height: 40px !important;
  }

  .topic-icon .icon-thumbs {
    width: 35px !important;
    height: 40px !important;
  }

  /* Info Block */
  .info-block {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
  }

  .info-icon {
    font-size: 22px;
    display: flex;
    align-items: center;
  }

  .info-icon img {
    width: 16px;
    height: 16px;
  }

  .about-text {
    margin: 0;
    line-height: 1.4;
    color: #333;
    font-size: 14px;
  }

  /* Post Comments */
  .post-comments {
    margin-top: 10px;
    border-top: 1px solid #ccc;
    padding-top: 20px;
  }
  
  .comment {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
  }
  
  .comment-content {
    background-color: #fff;
    border-radius: 10px;
    padding: 15px;
    flex: 1;
  }
  
  .comment-author {
    font-size: 16px;
    margin: 0 0 10px 0;
    font-weight: bold;
  }
  
  .comment-text {
    font-size: 14px;
    margin: 0;
    line-height: 1.4;
  }

  .nav-link {
    text-decoration: none;
  }

  .nav-button.active {
    background-color: #e0e0e0;
  }
</style>
