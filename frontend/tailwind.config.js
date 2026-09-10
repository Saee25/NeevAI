/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: 'var(--color-bg)',
        white: 'var(--color-bg-card)',
        sage: {
          DEFAULT: 'var(--color-primary)',
          light: 'var(--color-primary-light)',
        },
        gold: 'var(--color-accent)',
        charcoal: {
          DEFAULT: 'var(--color-text)',
          muted: 'var(--color-text-muted)',
        }
      },
      borderRadius: {
        DEFAULT: 'var(--radius)',
      },
      fontFamily: {
        serif: ['Fraunces', 'serif'],
        sans: ['Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
}
