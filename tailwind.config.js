/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './app_casamento/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Cormorant Garamond', 'serif'],
      },
      colors: {
        lavender: '#E6E6FA',
      },
    },
  },
  plugins: [],
}