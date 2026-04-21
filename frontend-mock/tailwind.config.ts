import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/app/**/*.{ts,tsx}", "./src/components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        pf: {
          black: "#0A0A0A",
          white: "#FFFFFF",
          "near-black": "#1A1A1A",
          muted: "#6B6B6B",
          border: "#E5E5E5",
          surface: "#F7F7F7",
          "gold-base": "#C9A227",
          income: "#1F7A3D",
          expense: "#B03A2E",
          warning: "#A87400",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "SF Pro", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "gold-metallic":
          "linear-gradient(135deg, #8B6914 0%, #B8922C 20%, #D4AF37 40%, #EDD060 50%, #D4AF37 60%, #B8922C 80%, #8B6914 100%)",
        "gold-metallic-subtle": "linear-gradient(135deg, #C9A227 0%, #E8D178 50%, #C9A227 100%)",
        "gold-text":
          "linear-gradient(135deg, #8B6914, #D4AF37 40%, #EDD060 50%, #D4AF37 60%, #8B6914)",
      },
      borderRadius: {
        card: "12px",
        sheet: "20px",
      },
    },
  },
  plugins: [],
};

export default config;
