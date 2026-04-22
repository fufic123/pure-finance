"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

export type ThemeMode = "light" | "dark" | "system";

type ThemeCtx = {
  /** Effective boolean — what the UI should render. */
  dark: boolean;
  /** The user's chosen mode (may be "system"). */
  mode: ThemeMode;
  setTheme: (t: ThemeMode) => void;
};

const STORAGE_KEY = "pf.theme";

const Ctx = createContext<ThemeCtx | null>(null);

function systemPrefersDark(): boolean {
  if (typeof window === "undefined") return false;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false;
}

function readStoredMode(): ThemeMode {
  if (typeof window === "undefined") return "system";
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (raw === "light" || raw === "dark" || raw === "system") return raw;
  return "system";
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  // Default is "system". Hydration-safe: first render assumes light (matches
  // the default SSR output). We re-sync against localStorage + prefers-color-scheme
  // on mount. A brief flicker on first paint is acceptable for a mock preview.
  const [mode, setMode] = useState<ThemeMode>("system");
  const [systemDark, setSystemDark] = useState<boolean>(false);
  const [mounted, setMounted] = useState(false);

  // Initial sync
  useEffect(() => {
    setMode(readStoredMode());
    setSystemDark(systemPrefersDark());
    setMounted(true);
  }, []);

  // Watch prefers-color-scheme changes.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => setSystemDark(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const setTheme = useCallback((t: ThemeMode) => {
    setMode(t);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(STORAGE_KEY, t);
    }
  }, []);

  const dark = mounted ? (mode === "system" ? systemDark : mode === "dark") : false;

  const value = useMemo<ThemeCtx>(() => ({ dark, mode, setTheme }), [dark, mode, setTheme]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useTheme(): ThemeCtx {
  const v = useContext(Ctx);
  if (!v) {
    // Fallback — used only if a component is rendered outside a provider
    // (e.g. during static analysis). Default to light.
    return { dark: false, mode: "system", setTheme: () => undefined };
  }
  return v;
}
