"use client";

import { useEffect } from "react";
import { useTheme } from "@/lib/theme";

/**
 * Mirror the effective theme onto <html data-pf-theme="..."> so globals.css
 * can style body bg/color appropriately without extra JS per page.
 */
export function ThemeHtmlSync() {
  const { dark } = useTheme();
  useEffect(() => {
    if (typeof document === "undefined") return;
    document.documentElement.setAttribute("data-pf-theme", dark ? "dark" : "light");
  }, [dark]);
  return null;
}
