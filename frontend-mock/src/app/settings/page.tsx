"use client";

import Link from "next/link";
import type { Route } from "next";
import { motion } from "framer-motion";
import { MOCK_USER } from "@/lib/mock";
import { GRAD_METALLIC, PF } from "@/lib/tokens";
import { PageTransition } from "@/components/page-transition";
import { TabBar } from "@/components/tab-bar";

type Row = {
  label: string;
  href?: Route;
  meta?: string;
  destructive?: boolean;
};

const TOP_ROWS: Row[] = [
  { label: "Banks & Sync", href: "/settings/banks" },
  { label: "Categories", href: "/settings/categories" },
  { label: "Rules", href: "/settings/rules" },
  { label: "Appearance", meta: "System" },
];

const DANGER_ROWS: Row[] = [{ label: "Log out", destructive: true }];

function ChevronRight() {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M9 18l6-6-6-6" />
    </svg>
  );
}

export default function SettingsPage() {
  return (
    <PageTransition>
      <main className="pf-safe-top min-h-screen bg-pf-black pb-[96px]">
        <header className="flex h-[52px] items-center justify-between px-5">
          <span className="text-[20px] font-semibold tracking-tight text-pf-white">Settings</span>
        </header>

        {/* Profile */}
        <section className="mx-5 mb-5 mt-2 flex items-center gap-3.5 rounded-[13px] border border-white/[0.08] bg-white/[0.03] p-4">
          <div
            className="flex h-12 w-12 items-center justify-center rounded-[12px] text-[18px] font-semibold text-pf-black"
            style={{ background: GRAD_METALLIC }}
          >
            {MOCK_USER.name.charAt(0)}
          </div>
          <div className="min-w-0 flex-1">
            <div className="truncate text-[16px] font-medium text-pf-white">{MOCK_USER.email}</div>
            <div className="text-[12px] text-white/40">{MOCK_USER.joined}</div>
          </div>
        </section>

        {/* Main group */}
        <Group>
          {TOP_ROWS.map((r, i) => (
            <SettingRow key={r.label} row={r} last={i === TOP_ROWS.length - 1} />
          ))}
        </Group>

        {/* Danger */}
        <Group>
          {DANGER_ROWS.map((r, i) => (
            <SettingRow key={r.label} row={r} last={i === DANGER_ROWS.length - 1} />
          ))}
        </Group>

        <p className="px-5 pb-8 pt-4 text-center text-[11px] text-white/25">
          Pure Finance · design preview
        </p>

        <TabBar />
      </main>
    </PageTransition>
  );
}

function Group({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-5 mb-5 overflow-hidden rounded-[13px] border border-white/[0.08] bg-white/[0.03]">
      {children}
    </div>
  );
}

function SettingRow({ row, last }: { row: Row; last: boolean }) {
  const content = (
    <motion.div
      whileTap={{ scale: 0.995 }}
      className={
        "flex h-12 items-center justify-between px-4 " +
        (last ? "" : "border-b border-white/[0.06]")
      }
    >
      <span
        className="text-[15px]"
        style={{ color: row.destructive ? PF.expense : "#FFFFFF" }}
      >
        {row.label}
      </span>
      <div className="flex items-center gap-2 text-white/40">
        {row.meta ? <span className="text-[14px]">{row.meta}</span> : null}
        {row.href ? <ChevronRight /> : null}
      </div>
    </motion.div>
  );

  return row.href ? (
    <Link href={row.href} className="block active:bg-white/[0.02]">
      {content}
    </Link>
  ) : (
    <button type="button" className="block w-full text-left active:bg-white/[0.02]">
      {content}
    </button>
  );
}
