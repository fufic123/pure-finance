import type { Metadata, Viewport } from "next";
import "./globals.css";
import { ThemeProvider } from "@/lib/theme";
import { ThemeHtmlSync } from "@/components/theme-html-sync";

export const metadata: Metadata = {
  title: "Pure Finance (mock)",
  description: "All your money, one clean view.",
  manifest: "/manifest.webmanifest",
  appleWebApp: {
    capable: true,
    title: "Pure Finance (mock)",
    statusBarStyle: "black-translucent",
  },
  formatDetection: { telephone: false },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#FFFFFF",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen font-sans">
        <ThemeProvider>
          <ThemeHtmlSync />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
