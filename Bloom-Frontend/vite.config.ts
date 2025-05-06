import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),  
    },
  },
  server: {
    proxy: {
      '/plants/search': 'http://localhost:8000',
      '/moisture': 'http://localhost:8000',
      '/evaluate_moisture/': 'http://localhost:8000',
      '/personal_plants/search': 'http://localhost:8000',
      '/personal_plants/create': 'http://localhost:8000',
      '/personal_plants/delete/': 'http://localhost:8000',
      '/personal_plants/assign_sensorID': 'http://localhost:8000',
      '/moisture/get_latest_moisture': 'http://localhost:8000',
      '/get_user_gardens': 'http://localhost:8000',
      '/get_garden': 'http://localhost:8000',
      '/create_garden': 'http://localhost:8000',
      '/delete_garden': 'http://localhost:8000',
      '/taken_sensors/': 'http://localhost:8000',
      '/get_status_history/': 'http://localhost:8000',
      '^/personal_plants/.*': 'http://localhost:8000',
    }
  }
})
