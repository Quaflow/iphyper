export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Serve HTML files with environment variable injection
    if (url.pathname === '/' || url.pathname === '/index.html') {
      // Create a new request explicitly for index.html
      const indexRequest = new Request(
        new URL('/index.html', url.origin),
        request
      );
      
      const response = await env.ASSETS.fetch(indexRequest);
      
      // Check if we got HTML content
      if (response.ok && response.headers.get('content-type')?.includes('text/html')) {
        let html = await response.text();
        
        // Inject environment variables
        const mapboxToken = env.MAPBOX_ACCESS_TOKEN || '';
        html = html.replace(/__MAPBOX_ACCESS_TOKEN__/g, mapboxToken);
        
        return new Response(html, {
          headers: {
            'content-type': 'text/html;charset=UTF-8',
            'cache-control': 'no-cache'
          }
        });
      }
      
      return response;
    }

    // Serve all other static assets normally
    return env.ASSETS.fetch(request);
  }
};
