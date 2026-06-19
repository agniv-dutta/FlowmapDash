/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FAF6F2',
          100: '#F8F6F3',
          200: '#F0EBE6',
          500: '#E58A69', // Match salmon/peach accent
          600: '#D67657',
          700: '#B55A3D',
        },
        accent: {
          teal: '#4A7C7E',
          sage: '#6B9F7C',
          rust: '#A85853',
          sand: '#D4A574',
        },
        neutral: {
          50: '#161618', // Dark background matching image
          100: '#212123', // Card background matching image
          200: '#2A2A2D', // Subtle borders/hover
          300: '#3D3D40',
          600: '#8A8A8E', // Secondary text
          900: '#F8F8F8', // Primary text
        },
      },
      boxShadow: {
        subtle: '0 2px 8px rgba(0, 0, 0, 0.2)',
        elevated: '0 4px 16px rgba(0, 0, 0, 0.4)',
      },
      borderRadius: {
        base: '6px',
        lg: '8px',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
