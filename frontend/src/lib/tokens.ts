export const PF = {
  black: "#0A0A0A",
  white: "#FFFFFF",
  nearBlack: "#1A1A1A",
  muted: "#6B6B6B",
  border: "#E5E5E5",
  surface: "#F7F7F7",
  goldBase: "#C9A227",
  income: "#1F7A3D",
  expense: "#B03A2E",
  warning: "#A87400",
} as const;

export const GRAD_METALLIC =
  "linear-gradient(135deg, #8B6914 0%, #B8922C 20%, #D4AF37 40%, #EDD060 50%, #D4AF37 60%, #B8922C 80%, #8B6914 100%)";

export const GRAD_METALLIC_SUBTLE =
  "linear-gradient(135deg, #C9A227 0%, #E8D178 50%, #C9A227 100%)";

export const GRAD_TEXT =
  "linear-gradient(135deg, #8B6914, #D4AF37 40%, #EDD060 50%, #D4AF37 60%, #8B6914)";

export const GOLD_TEXT_STYLE = {
  background: GRAD_TEXT,
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  WebkitTextFillColor: "transparent",
  display: "inline-block",
} as const;

export function pfTheme(dark: boolean) {
  return {
    bg: dark ? PF.black : PF.white,
    surface: dark ? PF.nearBlack : PF.surface,
    border: dark ? "#1F1F1F" : PF.border,
    text: dark ? PF.white : PF.black,
    muted: dark ? "rgba(255,255,255,0.4)" : PF.muted,
    subtleBorder: dark ? "#2A2A2A" : "#EEEEEE",
  };
}
