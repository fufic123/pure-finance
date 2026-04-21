"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { MOCK_ACCOUNTS, MOCK_CATEGORIES, MOCK_SUMMARY, MOCK_TRANSACTIONS, MOCK_USER } from "@/lib/mock";
import { PageTransition } from "@/components/page-transition";
import { StaggerList, staggerItem } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";
import { SummaryCard } from "@/components/summary-card";
import { AccountCard } from "@/components/account-card";
import { TransactionRow } from "@/components/transaction-row";
import { PF } from "@/lib/tokens";

export default function HomePage() {
  const today = new Date();
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const dayName = days[today.getDay()] ?? "Mon";
  const monthName = months[today.getMonth()] ?? "Apr";
  const dayNum = today.getDate();

  return (
    <PageTransition>
      <main className="pf-safe-top min-h-screen bg-pf-black pb-[96px]">
        <header className="flex h-[52px] items-center justify-between px-5">
          <span className="text-[17px] text-pf-white">
            Good morning, <span className="font-semibold">{MOCK_USER.name}.</span>
          </span>
          <div className="text-right">
            <div className="text-[11px] leading-tight text-white/40">{dayName}</div>
            <div className="text-[15px] font-semibold leading-tight tabular-nums text-pf-white">
              {dayNum} {monthName}
            </div>
          </div>
        </header>

        <SummaryCard summary={MOCK_SUMMARY} />

        <section className="pt-3.5">
          <SectionHead label="Accounts" action={<button className="text-[13px]" style={{ color: PF.goldBase }}>Sync all</button>} />
          <StaggerList className="mt-1">
            {MOCK_ACCOUNTS.map((acc) => (
              <AccountCard key={acc.id} account={acc} />
            ))}
            <motion.li variants={staggerItem} className="list-none">
              <Link
                href="/onboarding"
                className="flex h-[50px] items-center gap-3.5 px-5 text-white/40 active:bg-white/[0.02]"
              >
                <div className="flex h-[34px] w-[34px] flex-shrink-0 items-center justify-center rounded-[9px] border border-dashed border-white/25">
                  <span className="text-[18px] leading-none">+</span>
                </div>
                <span className="text-[15px]">Add bank</span>
              </Link>
            </motion.li>
          </StaggerList>
        </section>

        <section className="border-t border-white/[0.08] pt-3.5">
          <SectionHead label="This month" />
          <div className="px-5 pb-3 pt-1">
            {MOCK_CATEGORIES.slice(0, 3).map((cat, i) => (
              <motion.div
                key={cat.name}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.15, delay: i * 0.03 }}
                className={
                  "flex items-center justify-between py-2 " +
                  (i < 2 ? "border-b border-white/[0.06]" : "")
                }
              >
                <span className="text-[14px] text-pf-white">{cat.name}</span>
                <span className="text-[14px] tabular-nums text-white/45">−€{cat.total}</span>
              </motion.div>
            ))}
            <div className="pt-2">
              <Link href="/analytics" className="text-[13px]" style={{ color: PF.goldBase }}>
                See all in Analytics →
              </Link>
            </div>
          </div>
        </section>

        <section className="border-t border-white/[0.08] pt-3.5">
          <SectionHead
            label="Recent"
            action={
              <Link href="/transactions" className="text-[13px]" style={{ color: PF.goldBase }}>
                See all →
              </Link>
            }
          />
          <StaggerList className="mt-1">
            {MOCK_TRANSACTIONS.slice(0, 5).map((tx) => (
              <TransactionRow key={tx.id} tx={tx} />
            ))}
          </StaggerList>
        </section>

        <TabBar />
      </main>
    </PageTransition>
  );
}

function SectionHead({ label, action }: { label: string; action?: React.ReactNode }) {
  return (
    <div className="mb-1 flex items-center justify-between px-5">
      <span className="text-[15px] font-semibold text-pf-white">{label}</span>
      {action}
    </div>
  );
}
