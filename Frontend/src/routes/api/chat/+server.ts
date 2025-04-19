import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

// Обработчик POST-запросов для общения с LLM
export const POST: RequestHandler = async ({ request, fetch, locals }) => {
  try {
    const { message, chat_history } = await request.json();
    
    // Получаем заголовки авторизации из запроса
    const authHeader = request.headers.get('Authorization');
    
    // Проверка, что сообщение не пустое
    if (!message || typeof message !== 'string' || message.trim() === '') {
      return json({ error: 'Сообщение не может быть пустым' }, { status: 400 });
    }
    
    // Формируем текущий контекст для ассистента
    const context = 'Чат с ассистентом';
    
    // Подготавливаем заголовки
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };
    
    // Добавляем заголовок авторизации только если он есть
    if (authHeader) {
      headers['Authorization'] = authHeader;
    }
    
    // Отправляем запрос к бэкендовому ассистенту
    const response = await fetch('/api/assistant', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        prompt: message,
        context: context
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      return json({ 
        error: errorData.detail || 'Произошла ошибка при общении с ассистентом' 
      }, { status: response.status });
    }
    
    const data = await response.json();
    
    return json({
      response: data.answer
    });
  } catch (error) {
    console.error('Error in chat API:', error);
    return json({ 
      error: 'Внутренняя ошибка сервера' 
    }, { status: 500 });
  }
}; 