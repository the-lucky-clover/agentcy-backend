// agentcy-backend/src/index.ts
import { Router } from 'itty-router';
import { Database } from '@cloudflare/d1';

// Create a new router
const router = Router();

// Example: health check endpoint
router.get('/health', () => new Response('OK', { status: 200 }));

// Example: fetch all users from your D1 database
router.get('/users', async (req: Request, env: any) => {
  try {
    const db: Database = env.DB; // Your D1 binding
    const result = await db.prepare('SELECT * FROM users').all();
    return new Response(JSON.stringify(result.results), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: (err as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});

// Fallback route
router.all('*', () => new Response('Not Found', { status: 404 }));

export default {
  fetch: (request: Request, env: any, ctx: any) => router.handle(request, env),
};
