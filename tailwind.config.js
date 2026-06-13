/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/templates/*.html",
    "./app/static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        monetlink: {
          dark: '#0f0826',
          purple: '#1e0b4a',
          card: '#160d38',
          accent: '#facc15',
          panel: '#110a30',
          success: '#10b981',
          danger: '#f43f5e',
          warning: '#f59e0b',
          info: '#3b82f6'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'monospace'],
      },
      boxShadow: {
        'premium-glow': '0 0 25px -5px rgba(250, 204, 21, 0.15)',
        'card-glow': '0 10px 40px -10px rgba(15, 8, 38, 0.7)',
        'panel-inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.4)'
      },
      animation: {
        'gradient-pulse': 'gradientShift 8s ease infinite',
        'counter-spin': 'spinCounter 10s linear infinite'
      },
      keyframes: {
        gradientShift: {
          '0%, 100%': { 'background-position': '0% 50%' },
          '50%': { 'background-position': '100% 50%' },
        }
      }
    },
  },
  plugins: [],
}
