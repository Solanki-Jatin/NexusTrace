import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// This is the settings file for Vite, the tool that runs our React app
// during development and bundles it for production. You usually never
// need to touch this file.
export default defineConfig({
  plugins: [react()],
})
