import { writable } from 'svelte/store';
import { authStore } from './auth';

export interface AssistantPrompt {
  prompt: string;
  context: string;
}

export interface AssistantAnswer {
  answer: string;
}

export interface ChatMessage {
  sender: 'Student' | 'Assistant';
  content: string;
}

// Store for chat history
export const chatHistoryStore = writable<ChatMessage[]>([]);
export const isLoadingStore = writable<boolean>(false);

// Initialize chat history
export async function loadChatHistory(): Promise<void> {
  try {
    isLoadingStore.set(true);
    
    const token = await new Promise<string | null>(resolve => {
      authStore.token.subscribe(value => {
        resolve(value);
      })();
    });
    
    if (!token) {
      chatHistoryStore.set([]);
      return;
    }
    
    const response = await fetch('/api/assistant', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to load chat history');
    }
    
    const data = await response.json();
    
    if (data && data.length > 0 && data[0].messages) {
      const messages = data[0].messages;
      const formattedMessages: ChatMessage[] = [];
      
      for (let i = 0; i < messages.length; i++) {
        formattedMessages.push({
          sender: i % 2 === 0 ? 'Student' : 'Assistant',
          content: messages[i]
        });
      }
      
      chatHistoryStore.set(formattedMessages);
    } else {
      chatHistoryStore.set([]);
    }
  } catch (error) {
    console.error('Error loading chat history:', error);
    chatHistoryStore.set([]);
  } finally {
    isLoadingStore.set(false);
  }
}

// Send a message to the AI assistant
export async function sendMessage(message: string, context: string = ''): Promise<string | null> {
  try {
    isLoadingStore.set(true);
    
    const token = await new Promise<string | null>(resolve => {
      authStore.token.subscribe(value => {
        resolve(value);
      })();
    });
    
    if (!token) {
      throw new Error('Not authenticated');
    }
    
    // Add the user message to chat history immediately
    const userMessage: ChatMessage = {
      sender: 'Student',
      content: message
    };
    
    chatHistoryStore.update(history => [...history, userMessage]);
    
    const response = await fetch('/api/assistant', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt: message,
        context: context
      } as AssistantPrompt)
    });
    
    if (!response.ok) {
      throw new Error('Failed to get response from assistant');
    }
    
    const data: AssistantAnswer = await response.json();
    
    // Add the assistant's response to the chat history
    const assistantMessage: ChatMessage = {
      sender: 'Assistant',
      content: data.answer
    };
    
    chatHistoryStore.update(history => [...history, assistantMessage]);
    
    return data.answer;
  } catch (error) {
    console.error('Error sending message:', error);
    return null;
  } finally {
    isLoadingStore.set(false);
  }
}

// Clear chat history
export async function clearChatHistory(): Promise<boolean> {
  try {
    const token = await new Promise<string | null>(resolve => {
      authStore.token.subscribe(value => {
        resolve(value);
      })();
    });
    
    if (!token) {
      return false;
    }
    
    const response = await fetch('/api/assistant', {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to clear chat history');
    }
    
    chatHistoryStore.set([]);
    return true;
  } catch (error) {
    console.error('Error clearing chat history:', error);
    return false;
  }
}

// Get assistant hints for a specific context
export async function getHints(context: string): Promise<string[]> {
  try {
    const response = await fetch(`/api/assistant/hints?context=${encodeURIComponent(context)}`);
    
    if (!response.ok) {
      throw new Error('Failed to get hints');
    }
    
    const data = await response.json();
    return data.hints || [];
  } catch (error) {
    console.error('Error getting hints:', error);
    return [];
  }
} 