import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: true, // Necessário para Docker
        proxy: {
            // Redireciona chamadas para o NOVO backend Spring Boot (Porta 9999)
            '/api': {
                target: 'http://localhost:9999',
                changeOrigin: true,
                secure: false
            },
            '/graphql': {
                target: 'http://localhost:9999',
                changeOrigin: true,
                secure: false
            },
            '/login': {
                target: 'http://localhost:9999',
                changeOrigin: true,
                secure: false
            },
            '/usuarios': {
                target: 'http://localhost:9999',
                changeOrigin: true,
                secure: false
            }
        }
    }
})
