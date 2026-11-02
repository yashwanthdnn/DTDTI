/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          maroon: {
            DEFAULT: '#641E2B',
            dark: '#4A1520',
            light: '#85293A',
            50: '#FBF4F5',
            100: '#F5E6E8',
            200: '#E8C5CA',
            800: '#521823',
            900: '#3D121A',
          },
          cream: {
            DEFAULT: '#FFF8E8',
            light: '#FFFDF9',
            dark: '#F7EDD5',
          },
          gold: {
            DEFAULT: '#C69A45',
            light: '#DDB362',
            dark: '#A67D2F',
            50: '#FDF9F0',
            100: '#FBF2DD',
            500: '#C69A45',
          },
          brown: {
            DEFAULT: '#33251F',
            light: '#4D3A32',
            dark: '#221915',
            muted: '#6B5850',
          },
          green: {
            DEFAULT: '#2E7D32',
            light: '#4CAF50',
          }
        }
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(51, 37, 31, 0.08)',
        'card': '0 10px 30px -5px rgba(100, 30, 43, 0.08)',
        'gold': '0 4px 20px -2px rgba(198, 154, 69, 0.25)',
      }
    },
  },
  plugins: [],
}

