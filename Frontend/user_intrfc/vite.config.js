import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
// import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react()],

  // changes happend from here to integrate
  server: {
    proxy: {                                      // CHANGED FOR INTEGRATION
      '/api': {                                   // All calls starting with /api will go to backend
        target: 'http://127.0.0.1:8000',         // Backend address
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})