// src/index.ts

// Silence TypeScript errors for itty-router
declare module "itty-router";

import { Router } from "itty-router";
import { Database } from '@cloudflare/d1';

// Create a new router
const router = Router();

// Example: health check endpoint
router.get('/health', () => new Response('OK', { status: 200 }));

// Fetch all users from D1 database
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

// Upload a file to R2
router.post('/upload', async (req: Request, env: any) => {
  try {
    const r2Bucket = env.MY_R2_BUCKET; // R2 binding
    const formData = await req.formData();
    const file = formData.get('file') as File;
    if (!file) throw new Error('No file provided');

    const arrayBuffer = await file.arrayBuffer();
    await r2Bucket.put(file.name, arrayBuffer, {
      httpMetadata: { contentType: file.type },
    });

    return new Response(JSON.stringify({ success: true, filename: file.name }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: (err as Error).message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});

// Download a file from R2
router.get('/download/:filename', async (req: Request, env: any) => {
  try {
    const r2Bucket = env.MY_R2_BUCKET;
    const url = new URL(req.url);
    const filename = url.pathname.split('/').pop()!;
    const object = await r2Bucket.get(filename);

    if (!object) return new Response('File not found', { status: 404 });

    return new Response(object.body, {
      headers: { 'Content-Type': object.httpMetadata.contentType || 'application/octet-stream' },
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
