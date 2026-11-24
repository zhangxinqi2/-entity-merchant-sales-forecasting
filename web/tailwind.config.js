/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4CAF50',
        secondary: '#2196F3',
        accent: '#FF9800',
        success: '#4CAF50',
        warning: '#FF9800',
        danger: '#f44336',
      }
    },
  },
  plugins: [],
}
