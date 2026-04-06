import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// vite.config.js — as specified in Module 4 Section 12.3
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      }
    }
  }
})
