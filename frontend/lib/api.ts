import { getAuthToken } from './auth';
import { Task } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  
  // TypeScript error fix: Use Record<string, string> for headers
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    console.log(`Requesting: ${options.method || 'GET'} ${API_URL}${endpoint}`);
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'API request failed with no error message' }));
      console.error('API Error:', errorData);
      throw new Error(errorData.detail || 'API request failed');
    }

    if (response.status === 204) { // No Content
        return null as T;
    }
    
    const data = await response.json();
    console.log(`Response for ${endpoint}:`, data);
    return data;
  } catch (error) {
    console.error(`Error during API request to ${endpoint}:`, error);
    throw error;
  }
}

export async function getTasks(userId: number, filter?: 'all' | 'pending' | 'completed'): Promise<Task[]> {
  let endpoint = `/${userId}/tasks`;
  if (filter && filter !== 'all') {
    endpoint += `?completed=${filter === 'completed'}`;
  }
  return request<Task[]>(endpoint);
}

export async function createTask(userId: number, title: string, description: string): Promise<Task> {
    return request<Task>(`/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
}

export async function updateTask(userId: number, taskId: number, title: string, description: string): Promise<Task> {
    return request<Task>(`/${userId}/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify({ title, description }),
    });
}

export async function deleteTask(userId: number, taskId: number): Promise<void> {
    await request<null>(`/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
    });
}

export async function toggleComplete(userId: number, taskId: number): Promise<Task> {
    return request<Task>(`/${userId}/tasks/${taskId}/complete`, {
        method: 'PATCH',
    });
}

// Add the new chat function
export async function sendChatMessage(
  message: string,
  conversationId: number | null
): Promise<{ conversation_id: number; response: string }> {
  return request<{ conversation_id: number; response: string }>('/chat', {
    method: 'POST',
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
}