import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';

// Relative base: the built SPA is served from the FastAPI service, and may be
// embedded in a HAI-Chat thread iframe under an arbitrary path.
export default defineConfig({
    plugins: [react()],
    base: './',
    server: {
        port: 5174,
        proxy: {
            '/api': 'http://127.0.0.1:8091',
            '/ws': {target: 'ws://127.0.0.1:8091', ws: true},
        },
    },
});
