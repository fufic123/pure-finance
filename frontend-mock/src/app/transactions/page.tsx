"use client";

import { useState } from "react";
import { MOCK_TRANSACTIONS } from "@/lib/mock";
import { GRAD_METALLIC } from "@/lib/tokens";
import { PageTransition } from "@/components/page-transition";
import { StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";
import { TransactionRow } from "@/components/transaction-row";

const CHIPS = ["This month", "All accounts", "Food"] as const;

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
function IcSearch() {
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
      <circle cx="11" cy="11" r="8" />
      <path d="M21 21l-4.35-4.35" />
    </svg>
  );
}

export default function TransactionsPage() {
  const [active, setActive] = useState<(typeof CHIPS)[number]>("This month");

  return (
    <PageTransition>
      <main className="pf-safe-top min-h-screen bg-pf-black pb-[96px]">
        <header className="flex h-[52px] items-center justify-between px-5">
          <span className="text-[20px] font-semibold tracking-tight text-pf-white">Transactions</span>
          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-[10px] border border-white/[0.08] bg-white/[0.04] text-white/50 active:bg-white/[0.08]"
          >
            <IcFilter />
          </button>
        </header>

        <div className="pf-noscrollbar flex gap-2 overflow-x-auto px-5 pb-3">
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

        <div className="mx-5 mb-3 flex items-center gap-2.5 rounded-[10px] border border-white/[0.08] bg-white/[0.04] px-3.5 py-2 text-white/40">
          <IcSearch />
          <span className="text-[15px]">Search transactions</span>
        </div>

        <div className="mb-2 px-5">
          <span className="text-[12px] text-white/35">← Swipe a row to categorize</span>
        </div>

        <Group label="Today · Apr 21">
          {MOCK_TRANSACTIONS.slice(0, 2).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </Group>
        <Group label="Yesterday · Apr 20">
          {MOCK_TRANSACTIONS.slice(2, 3).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </Group>
        <Group label="Apr 19">
          {MOCK_TRANSACTIONS.slice(3, 5).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </Group>
        <Group label="Apr 18">
          {MOCK_TRANSACTIONS.slice(5, 6).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </Group>
        <Group label="Apr 17">
          {MOCK_TRANSACTIONS.slice(6, 7).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} />
          ))}
        </Group>

        <TabBar />
      </main>
    </PageTransition>
  );
}

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <section>
      <div className="mb-[2px] px-5 pt-3">
        <span className="text-[12px] font-medium uppercase tracking-[0.3px] text-white/40">
          {label}
        </span>
      </div>
      <StaggerList>{children}</StaggerList>
    </section>
  );
}
