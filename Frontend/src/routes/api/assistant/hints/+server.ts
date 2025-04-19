import { json, type RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ fetch, url }) => {
  try {
    const context = url.searchParams.get('context');
    
    if (!context) {
      return json({ error: 'Context parameter is required' }, { status: 400 });
    }
    
    const response = await fetch(`http://localhost:8000/assistant/hints?context=${encodeURIComponent(context)}`);
    
    const data = await response.json();
    
    if (!response.ok) {
      return json({ error: data.detail || 'Failed to get hints' }, { status: response.status });
    }
    
    return json(data);
  } catch (error) {
    console.error('Error in hints proxy:', error);
    return json({ error: 'Internal Server Error' }, { status: 500 });
  }
}; 