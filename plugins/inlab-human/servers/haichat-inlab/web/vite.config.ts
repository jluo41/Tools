import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';

// Relative base: the built SPA is served from the FastAPI service, and may be
// embedded in a HAI-Chat thread iframe under an arbitrary path.
export default defineConfig({
    plugins: [react()],
    base: './',
    build: {
        rollupOptions: {
            // plotly is most of the bundle and changes least: its own chunk, cached apart from the app
            output: {manualChunks: {plotly: ['plotly.js-dist-min']}},
        },
    },
    server: {
        port: 5174,
        proxy: {
            '/api': 'http://127.0.0.1:8091',
            '/ws': {target: 'ws://127.0.0.1:8091', ws: true},
        },
    },
});
