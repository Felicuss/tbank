import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ fetch, request }) => {
  try {
    const response = await fetch('http://localhost:8000/assistant', {
      headers: {
        Authorization: request.headers.get('Authorization') || '',
      },
    });

    const data = await response.json();
    
    if (!response.ok) {
      return json({ error: data.detail || 'Failed to get chat history' }, { status: response.status });
    }
    
    return json(data);
  } catch (error) {
    console.error('Error in assistant proxy:', error);
    return json({ error: 'Internal Server Error' }, { status: 500 });
  }
};

export const POST: RequestHandler = async ({ fetch, request }) => {
  try {
    const body = await request.json();
    
    const response = await fetch('http://localhost:8000/assistant', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: request.headers.get('Authorization') || '',
      },
      body: JSON.stringify(body),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      return json({ error: data.detail || 'Failed to get assistant response' }, { status: response.status });
    }
    
    return json(data);
  } catch (error) {
    console.error('Error in assistant proxy:', error);
    return json({ error: 'Internal Server Error' }, { status: 500 });
  }
};

export const DELETE: RequestHandler = async ({ fetch, request }) => {
  try {
    const response = await fetch('http://localhost:8000/assistant', {
      method: 'DELETE',
      headers: {
        Authorization: request.headers.get('Authorization') || '',
      },
    });
    
    if (!response.ok) {
      const data = await response.json();
      return json({ error: data.detail || 'Failed to delete chat history' }, { status: response.status });
    }
    
    return new Response(null, { status: 204 });
  } catch (error) {
    console.error('Error in assistant proxy:', error);
    return json({ error: 'Internal Server Error' }, { status: 500 });
  }
}; 