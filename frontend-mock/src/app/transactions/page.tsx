"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { MOCK_TRANSACTIONS } from "@/lib/mock";
import { GRAD_METALLIC, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";
import { TransactionRow } from "@/components/transaction-row";

const CHIPS = ["This month", "All accounts", "Food"] as const;
type Chip = (typeof CHIPS)[number];

function IcFilter({ color }: { color: string }) {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.6"
      strokeLinecap="round"
    >
      <line x1="4" y1="6" x2="20" y2="6" />
      <line x1="8" y1="12" x2="16" y2="12" />
      <line x1="11" y1="18" x2="13" y2="18" />
    </svg>
  );
}
function IcSearch({ color }: { color: string }) {
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
      <circle cx="11" cy="11" r="8" />
      <path d="M21 21l-4.35-4.35" />
    </svg>
  );
}

export default function TransactionsPage() {
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const [active, setActive] = useState<Chip>("This month");
  const [filterOpen, setFilterOpen] = useState(false);

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
            Transactions
          </span>
          <motion.button
            type="button"
            whileTap={{ scale: 0.92 }}
            onClick={() => setFilterOpen(true)}
            className="flex h-9 w-9 items-center justify-center rounded-[10px]"
            style={{
              background: C.surface,
              border: `1px solid ${C.border}`,
              color: C.muted,
            }}
          >
            <IcFilter color={C.muted} />
          </motion.button>
        </header>

        <div className="pf-noscrollbar flex gap-2 overflow-x-auto px-5 pb-3">
          {CHIPS.map((chip) => {
            const on = chip === active;
            return (
              <button
                key={chip}
                type="button"
                onClick={() => setActive(chip)}
                className="flex-shrink-0 rounded-full px-3 py-[5px] text-[13px] font-medium transition"
                style={
                  on
                    ? { background: GRAD_METALLIC, color: "#000" }
                    : {
                        background: dark ? "#1A1A1A" : "#F0F0F0",
                        border: `1px solid ${C.border}`,
                        color: C.muted,
                      }
                }
              >
                {chip}
              </button>
            );
          })}
        </div>

        <div
          className="mx-5 mb-3 flex items-center gap-2.5 rounded-[10px] px-3.5 py-2"
          style={{
            background: C.surface,
            border: `1px solid ${C.border}`,
          }}
        >
          <IcSearch color={C.muted} />
          <span className="text-[15px]" style={{ color: C.muted }}>
            Search transactions
          </span>
        </div>

        <div className="mb-2 px-5">
          <span className="text-[12px]" style={{ color: C.muted }}>
            ← Swipe a row to categorize
          </span>
        </div>

        <Group label="Today · Apr 21" dark={dark}>
          {MOCK_TRANSACTIONS.slice(0, 2).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} dark={dark} />
          ))}
        </Group>
        <Group label="Yesterday · Apr 20" dark={dark}>
          {MOCK_TRANSACTIONS.slice(2, 3).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} dark={dark} />
          ))}
        </Group>
        <Group label="Apr 19" dark={dark}>
          {MOCK_TRANSACTIONS.slice(3, 5).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} dark={dark} />
          ))}
        </Group>
        <Group label="Apr 18" dark={dark}>
          {MOCK_TRANSACTIONS.slice(5, 6).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} dark={dark} />
          ))}
        </Group>
        <Group label="Apr 17" dark={dark}>
          {MOCK_TRANSACTIONS.slice(6, 7).map((tx) => (
            <TransactionRow key={tx.id} tx={tx} dark={dark} />
          ))}
        </Group>

        <AnimatePresence>
          {filterOpen ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="pf-safe-bottom fixed inset-0 z-[60] flex items-end bg-black/50"
              onClick={() => setFilterOpen(false)}
            >
              <motion.div
                initial={{ y: 300 }}
                animate={{ y: 0 }}
                exit={{ y: 300 }}
                transition={{ duration: 0.22, ease: "easeOut" }}
                onClick={(e) => e.stopPropagation()}
                className="w-full rounded-t-[20px] p-5"
                style={{
                  background: C.bg,
                  border: `1px solid ${C.border}`,
                }}
              >
                <div
                  className="mx-auto mb-4 h-1 w-10 rounded-full"
                  style={{ background: C.border }}
                />
                <h3
                  className="mb-3 text-[17px] font-semibold"
                  style={{ color: C.text }}
                >
                  Filter
                </h3>
                <div className="flex flex-col gap-2">
                  {CHIPS.map((chip) => {
                    const on = chip === active;
                    return (
                      <button
                        key={chip}
                        type="button"
                        onClick={() => {
                          setActive(chip);
                          setFilterOpen(false);
                        }}
                        className="flex h-12 items-center justify-between rounded-[10px] px-3.5 text-left text-[15px]"
                        style={{
                          border: `1px solid ${C.border}`,
                          color: C.text,
                          background: on ? C.surface : "transparent",
                        }}
                      >
                        {chip}
                        {on ? (
                          <span style={{ fontSize: 14, color: "#C9A227" }}>✓</span>
                        ) : null}
                      </button>
                    );
                  })}
                </div>
              </motion.div>
            </motion.div>
          ) : null}
        </AnimatePresence>

        <TabBar />
      </main>
    </PageTransition>
  );
}

function Group({
  label,
  dark,
  children,
}: {
  label: string;
  dark: boolean;
  children: React.ReactNode;
}) {
  const C = pfTheme(dark);
  return (
    <section>
      <div className="mb-[2px] px-5 pt-3">
        <span
          className="text-[12px] font-medium uppercase tracking-[0.3px]"
          style={{ color: C.muted }}
        >
          {label}
        </span>
      </div>
      <StaggerList>{children}</StaggerList>
    </section>
  );
}
