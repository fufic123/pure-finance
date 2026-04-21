"use client";

import Link from "next/link";
import { useState } from "react";
import { MOCK_CATEGORIES } from "@/lib/mock";
import { GRAD_METALLIC, PF } from "@/lib/tokens";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";
import { DonutChart } from "@/components/donut-chart";
import { CategoryBar } from "@/components/category-bar";

const CHIPS = ["This month", "All accounts", "April 2026"] as const;

// Grayscale-ish palette, ordered by rank.
const DOTS = ["#F0F0F0", "#BFBFBF", "#8E8E8E", "#5C5C5C", "#3A3A3A"];

function IcFilter() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    >
      <line x1="4" y1="6" x2="20" y2="6" />
      <line x1="8" y1="12" x2="16" y2="12" />
      <line x1="11" y1="18" x2="13" y2="18" />
    </svg>
  );
}

export default function AnalyticsPage() {
  const [active, setActive] = useState<(typeof CHIPS)[number]>("This month");
  const [focused, setFocused] = useState<number | undefined>(undefined);

  const spendable = MOCK_CATEGORIES.filter((c) => c.name !== "Uncategorized");
  const uncategorized = MOCK_CATEGORIES.find((c) => c.name === "Uncategorized");

  const segments = spendable.map((cat, i) => ({
    label: cat.name,
    pct: cat.pct,
    color: DOTS[i] ?? "#5C5C5C",
  }));

  return (
    <PageTransition>
      <main className="pf-safe-top min-h-screen bg-pf-black pb-[96px]">
        <header className="flex h-[52px] items-center justify-between px-5">
          <span className="text-[20px] font-semibold tracking-tight text-pf-white">Analytics</span>
          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-[10px] border border-white/[0.08] bg-white/[0.04] text-white/50 active:bg-white/[0.08]"
          >
            <IcFilter />
          </button>
        </header>

        <div className="pf-noscrollbar flex gap-2 overflow-x-auto px-5 pb-4">
          {CHIPS.map((chip) => {
            const on = chip === active;
            return (
              <button
                key={chip}
                type="button"
                onClick={() => setActive(chip)}
                className={
                  "flex-shrink-0 rounded-full px-3 py-[5px] text-[13px] font-medium transition " +
                  (on ? "text-pf-black" : "border border-white/[0.08] bg-white/[0.04] text-white/50")
                }
                style={on ? { background: GRAD_METALLIC } : undefined}
              >
                {chip}
              </button>
            );
          })}
        </div>

        <section className="flex flex-col items-center gap-4 px-5 pb-6">
          <DonutChart
            segments={segments}
            centerLabel="−€1,540"
            centerSub="April"
            focusedIndex={focused}
          />
          <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1.5">
            {segments.map((seg, i) => (
              <button
                key={seg.label}
                type="button"
                onClick={() => setFocused(focused === i ? undefined : i)}
                className="flex items-center gap-1.5"
              >
                <span
                  className="inline-block h-2 w-2 rounded-[2px]"
                  style={{ background: seg.color }}
                />
                <span className="text-[12px] text-white/60">{seg.label}</span>
                <span className="text-[12px] tabular-nums text-white/40">{seg.pct}%</span>
              </button>
            ))}
          </div>
        </section>

        <div className="mb-2 px-5">
          <span className="text-[15px] font-semibold text-pf-white">By category</span>
        </div>
        <StaggerList>
          {spendable.map((cat, i) => (
            <StaggerItem key={cat.name} className="list-none">
              <CategoryBar
                name={cat.name}
                count={cat.count}
                total={cat.total}
                pct={cat.pct}
                dotColor={DOTS[i] ?? "#5C5C5C"}
              />
            </StaggerItem>
          ))}
          {uncategorized ? (
            <StaggerItem className="list-none">
              <div className="border-b border-white/[0.06] px-5 py-3">
                <CategoryBar
                  name={uncategorized.name}
                  count={uncategorized.count}
                  total={uncategorized.total}
                  pct={uncategorized.pct}
                  dotColor="#3A3A3A"
                  muted
                />
                <div className="mt-2 pl-4">
                  <Link
                    href="/transactions"
                    className="text-[13px]"
                    style={{ color: PF.goldBase }}
                  >
                    Assign categories →
                  </Link>
                </div>
              </div>
            </StaggerItem>
          ) : null}
        </StaggerList>

        <TabBar />
      </main>
    </PageTransition>
  );
}
