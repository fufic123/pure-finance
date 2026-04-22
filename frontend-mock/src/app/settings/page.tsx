"use client";

import Link from "next/link";
import type { Route } from "next";
import { motion } from "framer-motion";
import { MOCK_USER } from "@/lib/mock";
import { GRAD_METALLIC, PF, pfTheme } from "@/lib/tokens";
import { useTheme, type ThemeMode } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { TabBar } from "@/components/tab-bar";

function ChevronRight({ color }: { color: string }) {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M9 18l6-6-6-6" />
    </svg>
  );
}

const MODES: { key: ThemeMode; label: string }[] = [
  { key: "system", label: "System" },
  { key: "light", label: "Light" },
  { key: "dark", label: "Dark" },
];

export default function SettingsPage() {
  const { dark, mode, setTheme } = useTheme();
  const C = pfTheme(dark);

  return (
    <PageTransition>
      <main
        className="pf-safe-top min-h-screen pb-[96px]"
        style={{ background: C.bg }}
      >
        <header className="flex h-[52px] items-center justify-between px-5">
          <span
            className="text-[20px] font-semibold tracking-tight"
            style={{ color: C.text }}
          >
            Settings
          </span>
        </header>

        {/* Profile */}
        <section
          className="mx-5 mb-5 mt-2 flex items-center gap-3.5 rounded-[13px] p-4"
          style={{
            border: `1px solid ${C.border}`,
            background: dark ? "#1A1A1A" : "#F7F7F7",
          }}
        >
          <div
            className="flex h-12 w-12 items-center justify-center rounded-[12px] text-[18px] font-semibold"
            style={{ background: GRAD_METALLIC, color: "#0A0A0A" }}
          >
            {MOCK_USER.name.charAt(0)}
          </div>
          <div className="min-w-0 flex-1">
            <div
              className="truncate text-[16px] font-medium"
              style={{ color: C.text }}
            >
              {MOCK_USER.email}
            </div>
            <div className="text-[12px]" style={{ color: C.muted }}>
              {MOCK_USER.joined}
            </div>
          </div>
        </section>

        <Group dark={dark}>
          <LinkRow label="Banks & Sync" href="/settings/banks" dark={dark} />
          <LinkRow label="Categories" href="/settings/categories" dark={dark} />
          <LinkRow label="Rules" href="/settings/rules" dark={dark} last />
        </Group>

        {/* Appearance group — theme switcher */}
        <Group dark={dark}>
          <div className="px-4 pt-3 pb-1">
            <span
              className="text-[12px] font-medium uppercase tracking-[0.3px]"
              style={{ color: C.muted }}
            >
              Appearance
            </span>
          </div>
          <div className="px-3 pb-3">
            <div
              className="flex rounded-[10px] p-1"
              style={{ background: dark ? "#0A0A0A" : "#FFFFFF" }}
            >
              {MODES.map((m) => {
                const on = m.key === mode;
                return (
                  <button
                    key={m.key}
                    type="button"
                    onClick={() => setTheme(m.key)}
                    className="flex-1 rounded-[8px] py-2 text-[13px] font-medium"
                    style={{
                      background: on ? (dark ? "#1F1F1F" : "#F0F0F0") : "transparent",
                      color: on ? C.text : C.muted,
                    }}
                  >
                    {m.label}
                  </button>
                );
              })}
            </div>
          </div>
        </Group>

        {/* Danger */}
        <Group dark={dark}>
          <ButtonRow label="Log out" dark={dark} destructive last />
        </Group>

        <p
          className="px-5 pb-8 pt-4 text-center text-[11px]"
          style={{ color: C.muted }}
        >
          Pure Finance · design preview
        </p>

        <TabBar />
      </main>
    </PageTransition>
  );
}

function Group({
  children,
  dark,
}: {
  children: React.ReactNode;
  dark: boolean;
}) {
  const C = pfTheme(dark);
  return (
    <div
      className="mx-5 mb-5 overflow-hidden rounded-[13px]"
      style={{
        border: `1px solid ${C.border}`,
        background: dark ? "#1A1A1A" : "#F7F7F7",
      }}
    >
      {children}
    </div>
  );
}

function LinkRow({
  label,
  href,
  dark,
  last = false,
}: {
  label: string;
  href: Route;
  dark: boolean;
  last?: boolean;
}) {
  const C = pfTheme(dark);
  return (
    <Link href={href} className="block">
      <motion.div
        whileTap={{ scale: 0.995 }}
        className="flex h-12 items-center justify-between px-4"
        style={{
          borderBottom: last ? "none" : `1px solid ${C.subtleBorder}`,
        }}
      >
        <span className="text-[15px]" style={{ color: C.text }}>
          {label}
        </span>
        <ChevronRight color={C.muted} />
      </motion.div>
    </Link>
  );
}

function ButtonRow({
  label,
  dark,
  destructive = false,
  last = false,
}: {
  label: string;
  dark: boolean;
  destructive?: boolean;
  last?: boolean;
}) {
  const C = pfTheme(dark);
  return (
    <button type="button" className="block w-full text-left">
      <motion.div
        whileTap={{ scale: 0.995 }}
        className="flex h-12 items-center justify-between px-4"
        style={{
          borderBottom: last ? "none" : `1px solid ${C.subtleBorder}`,
        }}
      >
        <span
          className="text-[15px]"
          style={{ color: destructive ? PF.expense : C.text }}
        >
          {label}
        </span>
      </motion.div>
    </button>
  );
}
