"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  MOCK_ACCOUNTS,
  MOCK_TRANSACTIONS,
} from "@/lib/mock";
import { GOLD_TEXT_STYLE, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { StaggerList } from "@/components/stagger-list";
import { OutlineButton } from "@/components/outline-button";
import { TransactionRow } from "@/components/transaction-row";
import { AccAICard } from "@/components/acc-ai-card";
import { ActionSheet } from "@/components/action-sheet";
import { ConfirmSheet } from "@/components/confirm-sheet";

function IcChevronLeft({ color }: { color: string }) {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M15 18l-6-6 6-6" />
    </svg>
  );
}

function IcRefresh({ color }: { color: string }) {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
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
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const acc = MOCK_ACCOUNTS[0]!;
  const [syncing, setSyncing] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const handleSync = () => {
    if (syncing) return;
    setSyncing(true);
    window.setTimeout(() => setSyncing(false), 1000);
  };

  return (
    <PageTransition>
      <main className="min-h-screen pb-20" style={{ background: C.bg }}>
        {/* Top bar */}
        <div className="flex h-[52px] items-center justify-between px-4">
          <button
            type="button"
            onClick={() => router.back()}
            className="flex items-center gap-0.5"
            style={{ color: C.muted }}
          >
            <IcChevronLeft color={C.muted} />
            <span className="text-[15px]">Back</span>
          </button>
          <span
            className="text-[17px] font-semibold"
            style={{ color: C.text }}
          >
            {acc.name}
          </span>
          <button
            type="button"
            onClick={() => setMenuOpen(true)}
            aria-label="More"
            className="flex h-9 w-9 items-center justify-center rounded-[10px]"
            style={{
              background: C.surface,
              border: `1px solid ${C.border}`,
            }}
          >
            <svg width="18" height="4" viewBox="0 0 18 4" fill={C.muted}>
              <circle cx="2" cy="2" r="2" />
              <circle cx="9" cy="2" r="2" />
              <circle cx="16" cy="2" r="2" />
            </svg>
          </button>
        </div>

        <ActionSheet
          open={menuOpen}
          onClose={() => setMenuOpen(false)}
          actions={[
            { label: "Edit account", onClick: () => router.push(`/accounts/${acc.id}/edit`) },
            { label: "Delete account", destructive: true, onClick: () => setConfirmDelete(true) },
          ]}
        />
        <ConfirmSheet
          open={confirmDelete}
          title="Delete this account?"
          body="All transactions and balance snapshots linked to this account will be removed."
          confirmLabel="Delete"
          destructive
          onClose={() => setConfirmDelete(false)}
          onConfirm={() => router.push("/home")}
        />

        {/* Balance hero */}
        <section className="px-5 pb-6 pt-4 text-center">
          <div
            className="mb-2.5 text-[12px] uppercase tracking-[0.6px]"
            style={{ color: C.muted }}
          >
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
          <div className="mt-2 text-[13px]" style={{ color: C.muted }}>
            {acc.currency} account
          </div>
          <div
            className="mt-1 text-[12px]"
            style={{ color: C.muted, opacity: 0.7 }}
          >
            Last synced 3h ago
          </div>
        </section>

        <div className="px-5 pb-5">
          <OutlineButton dark={dark} onClick={handleSync} disabled={syncing}>
            {syncing ? (
              <span className="flex items-center gap-2">
                <span
                  className="inline-block h-3.5 w-3.5 rounded-full"
                  style={{
                    border: "2px solid",
                    borderColor: `${C.muted} ${C.muted} ${C.muted} transparent`,
                    animation: "pf-spin 0.7s linear infinite",
                  }}
                />
                Syncing…
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <IcRefresh color={C.text} />
                Sync
              </span>
            )}
          </OutlineButton>
        </div>

        <div className="px-5 pb-5">
          <Link
            href="/transactions/new"
            className="flex h-11 w-full items-center justify-center gap-2 rounded-[12px] text-[14px] font-medium"
            style={{
              border: `1.5px solid ${C.border}`,
              color: C.text,
            }}
          >
            <span className="text-[18px] font-light leading-none">+</span>
            Add transaction
          </Link>
        </div>

        <div className="mx-5 mb-4 h-px" style={{ background: C.border }} />

        {/* Analytics — AI Insights */}
        <AccAICard dark={dark} />

        {/* Transactions */}
        <div className="mb-1 flex items-center justify-between px-5">
          <span
            className="text-[15px] font-semibold"
            style={{ color: C.text }}
          >
            Transactions · Apr 2026
          </span>
        </div>
        <StaggerList className="mt-1">
          {MOCK_TRANSACTIONS.map((tx) => (
            <TransactionRow key={tx.id} tx={tx} dark={dark} />
          ))}
        </StaggerList>
      </main>
    </PageTransition>
  );
}
