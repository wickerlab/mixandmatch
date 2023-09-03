// vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: 'src/main.jsx', // Adjust this to your main entry file
      },
    },
  },
  optimizeDeps: {
    include: ['vue'], // Example: Specify dependencies to optimize
  },
})
