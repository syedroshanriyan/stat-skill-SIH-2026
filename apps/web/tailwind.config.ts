import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#171717",
        "warm-ivory": "#F7F3EA",
        paper: "#FCFAF5",
        charcoal: "#2A2A2A",
        forest: {
          DEFAULT: "#1F4D3A",
          light: "#28664D",
          dark: "#143326"
        },
        sage: {
          DEFAULT: "#A7B9A7",
          light: "#C5D4C5",
          dark: "#819781"
        },
        gold: {
          DEFAULT: "#B38A3E",
          light: "#CF9F47",
          dark: "#8F6E32"
        },
        terracotta: {
          DEFAULT: "#A85D45",
          light: "#C26D51",
          dark: "#824632"
        }
      },
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", "Inter", "system-ui", "-apple-system", "sans-serif"],
        serif: ["'Playfair Display'", "DM Serif Display", "Georgia", "serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        card: "0 1px 3px rgba(23, 23, 23, 0.05), 0 1px 2px rgba(23, 23, 23, 0.03)",
        elevated: "0 4px 6px -1px rgba(23, 23, 23, 0.06), 0 2px 4px -1px rgba(23, 23, 23, 0.03)",
      }
    },
  },
  plugins: [],
};
export default config;
