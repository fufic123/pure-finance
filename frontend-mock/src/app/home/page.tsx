"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  MOCK_ACCOUNTS,
  MOCK_CATEGORIES,
  MOCK_SUMMARY,
  MOCK_TRANSACTIONS,
  MOCK_USER,
} from "@/lib/mock";
import { PageTransition } from "@/components/page-transition";
import { StaggerList, staggerItem } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";
import { SummaryCard } from "@/components/summary-card";
import { AccountCard } from "@/components/account-card";
import { TransactionRow } from "@/components/transaction-row";
import { PF, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

export default function HomePage() {
  const { dark } = useTheme();
  const C = pfTheme(dark);

  const today = new Date();
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const dayName = days[today.getDay()] ?? "Mon";
  const monthName = months[today.getMonth()] ?? "Apr";
  const dayNum = today.getDate();

  return (
    <PageTransition>
      <main
        className="pf-safe-top min-h-screen pb-[96px]"
        style={{ background: C.bg }}
      >
        <header className="flex h-[52px] items-center justify-between px-5">
          <span className="text-[17px]" style={{ color: C.text }}>
            Good morning, <span className="font-semibold">{MOCK_USER.name}.</span>
          </span>
          <div className="text-right">
            <div className="text-[11px] leading-tight" style={{ color: C.muted }}>
              {dayName}
            </div>
            <div
              className="text-[15px] font-semibold leading-tight tabular-nums"
              style={{ color: C.text }}
            >
              {dayNum} {monthName}
            </div>
          </div>
        </header>

        <SummaryCard summary={MOCK_SUMMARY} dark={dark} />

        <section className="pt-3.5">
          <SectionHead
            label="Accounts"
            action={
              <button
                type="button"
                className="text-[13px]"
                style={{ color: PF.goldBase, background: "transparent" }}
              >
                Sync all
              </button>
            }
            dark={dark}
          />
          <StaggerList className="mt-1">
            {MOCK_ACCOUNTS.map((acc) => (
              <AccountCard key={acc.id} account={acc} dark={dark} />
            ))}
            <motion.li variants={staggerItem} className="list-none">
              <Link
                href="/onboarding"
                className="flex h-[50px] items-center gap-3.5 px-5"
                style={{ color: C.muted }}
              >
                <div
                  className="flex h-[34px] w-[34px] flex-shrink-0 items-center justify-center rounded-[9px]"
                  style={{ border: `1.5px dashed ${C.border}` }}
                >
                  <span className="text-[18px] leading-none">+</span>
                </div>
                <span className="text-[15px]">Add bank</span>
              </Link>
            </motion.li>
          </StaggerList>
        </section>

        <section
          className="pt-3.5"
          style={{ borderTop: `1px solid ${C.border}` }}
        >
          <SectionHead label="This month" dark={dark} />
          <Link href="/analytics" className="block px-5 pb-3 pt-1">
            {MOCK_CATEGORIES.slice(0, 3).map((cat, i) => (
              <motion.div
                key={cat.name}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.15, delay: i * 0.03 }}
                className="flex items-center justify-between py-2"
                style={{
                  borderBottom: i < 2 ? `1px solid ${C.subtleBorder}` : "none",
                }}
              >
                <span className="text-[14px]" style={{ color: C.text }}>
                  {cat.name}
                </span>
                <span
                  className="text-[14px] tabular-nums"
                  style={{ color: C.muted }}
                >
                  −€{cat.total}
                </span>
              </motion.div>
            ))}
            <div className="pt-2">
              <span className="text-[13px]" style={{ color: PF.goldBase }}>
                See all in Analytics →
              </span>
            </div>
          </Link>
        </section>

        <section
          className="pt-3.5"
          style={{ borderTop: `1px solid ${C.border}` }}
        >
          <SectionHead
            label="Recent"
            action={
              <Link
                href="/transactions"
                className="text-[13px]"
                style={{ color: PF.goldBase }}
              >
                See all →
              </Link>
            }
            dark={dark}
          />
          <StaggerList className="mt-1">
            {MOCK_TRANSACTIONS.slice(0, 5).map((tx) => (
              <TransactionRow key={tx.id} tx={tx} dark={dark} />
            ))}
          </StaggerList>
        </section>

        <TabBar />
      </main>
    </PageTransition>
  );
}

function SectionHead({
  label,
  action,
  dark,
}: {
  label: string;
  action?: React.ReactNode;
  dark: boolean;
}) {
  const C = pfTheme(dark);
  return (
    <div className="mb-1 flex items-center justify-between px-5">
      <span className="text-[15px] font-semibold" style={{ color: C.text }}>
        {label}
      </span>
      {action}
    </div>
  );
}
