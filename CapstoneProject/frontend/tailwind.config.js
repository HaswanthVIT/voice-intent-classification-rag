/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        base: "#0D0F14",
        surface: "#151820",
        elevated: "#1E2130",
        border: "#2A2D3E",
        primary: "#E8EAF6",
        secondary: "#8B90B0",
        blue: "#4FC3F7",
        green: "#69F0AE",
        amber: "#FFD740",
        red: "#FF5252",
        purple: "#CE93D8",
        customer: "#80DEEA",
        agent: "#BCAAA4"
      }
    }
  },
  plugins: [],
};