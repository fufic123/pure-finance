"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { MOCK_ACCOUNTS, MOCK_CATEGORIES, MOCK_SUMMARY, MOCK_TRANSACTIONS } from "@/lib/mock";
import { GOLD_TEXT_STYLE, GRAD_METALLIC_SUBTLE, PF } from "@/lib/tokens";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerList } from "@/components/stagger-list";
import { OutlineButton } from "@/components/outline-button";
import { TransactionRow } from "@/components/transaction-row";

function IcRefresh() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
    >
      <path d="M23 4v6h-6" />
      <path d="M1 20v-6h6" />
      <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" />
    </svg>
  );
}

export default function AccountDetailPage() {
  const acc = MOCK_ACCOUNTS[0]!;
  const [syncing, setSyncing] = useState(false);

  const handleSync = () => {
    setSyncing(true);
    window.setTimeout(() => setSyncing(false), 2200);
  };

  return (
    <PageTransition>
      <main className="min-h-screen bg-pf-black pb-20">
        <TopBar title={acc.name} back="/home" />

        {/* Balance hero */}
        <section className="px-5 pb-6 pt-4 text-center">
          <div className="mb-2.5 text-[12px] uppercase tracking-[0.6px] text-white/45">
            Balance
          </div>
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: "easeOut", delay: 0.05 }}
            className="text-[44px] font-bold leading-none tracking-[-1.5px] tabular-nums"
            style={GOLD_TEXT_STYLE}
          >
            €{acc.balance}
          </motion.div>
          <div className="mt-2 text-[13px] text-white/45">{acc.currency} account</div>
          <div className="mt-1 text-[12px] text-white/30">Last synced 3h ago</div>
        </section>

        <div className="px-5 pb-5">
          <OutlineButton onClick={handleSync} disabled={syncing}>
            {syncing ? (
              <span className="flex items-center gap-2">
                <span className="inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/50 border-t-transparent" />
                Syncing…
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <IcRefresh />
                Sync
              </span>
            )}
          </OutlineButton>
        </div>

        <div className="mx-5 mb-4 h-px bg-white/[0.08]" />

        {/* Stats card (ported from AccStatsCard) */}
        <div className="mx-5 mb-5 rounded-[13px] border border-white/[0.08] bg-white/[0.03] p-4">
          <div className="mb-3.5 text-[12px] font-semibold uppercase tracking-[0.4px] text-white/45">
            April 2026
          </div>
          <div className="mb-3.5 flex justify-between">
            <Stat label="Spent" value={`−€${MOCK_SUMMARY.expenses}`} color={PF.expense} align="left" />
            <Stat label="Transactions" value={`${MOCK_SUMMARY.count}`} color={PF.white} align="center" />
            <Stat label="Avg / day" value="€51" color={PF.white} align="right" />
          </div>
          <div className="border-t border-white/[0.08]">
            {MOCK_CATEGORIES.slice(0, 4).map((cat, i) => (
              <div
                key={cat.name}
                className={
                  "flex items-center justify-between py-[7px] " +
                  (i < 3 ? "border-b border-white/[0.04]" : "")
                }
              >
                <div className="flex items-center gap-2">
                  <span
                    className="inline-block h-[7px] w-[7px] rounded-full"
                    style={{
                      background: ["#F0F0F0", "#AAAAAA", "#7A7A7A", "#555555"][i] ?? "#555555",
                    }}
                  />
                  <span className="text-[13px] text-pf-white">{cat.name}</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <div className="h-[2px] w-12 overflow-hidden rounded-[1px] bg-white/[0.08]">
                    <div
                      className="h-full rounded-[1px]"
                      style={{ width: `${cat.pct}%`, background: GRAD_METALLIC_SUBTLE }}
                    />
                  </div>
                  <span className="w-14 text-right text-[13px] tabular-nums text-white/45">
                    −€{cat.total}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Transactions */}
        <div className="mb-1 flex items-center justify-between px-5">
          <span className="text-[15px] font-semibold text-pf-white">
            Transactions · Apr 2026
          </span>
        </div>
        <StaggerList className="mt-1">
          {MOCK_TRANSACTIONS.map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </StaggerList>
      </main>
    </PageTransition>
  );
}

function Stat({
  label,
  value,
  color,
  align,
}: {
  label: string;
  value: string;
  color: string;
  align: "left" | "center" | "right";
}) {
  const alignClass =
    align === "left" ? "text-left" : align === "right" ? "text-right" : "text-center";
  return (
    <div className={alignClass}>
      <div className="mb-[3px] text-[11px] text-white/45">{label}</div>
      <div
        className="text-[15px] font-semibold tabular-nums"
        style={{ color }}
      >
        {value}
      </div>
    </div>
  );
}
