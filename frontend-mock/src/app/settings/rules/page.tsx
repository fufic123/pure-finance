"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { MOCK_RULES, MOCK_CATEGORY_TREE } from "@/lib/mock";
import { PF } from "@/lib/tokens";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";

type SheetState = {
  open: boolean;
  keyword: string;
  category: string;
};

// Flatten the category tree for the picker so users can pick a leaf.
const CATEGORY_OPTIONS: string[] = MOCK_CATEGORY_TREE.flatMap((parent) =>
  parent.children.length
    ? parent.children.map((child) => `${parent.name} · ${child.name}`)
    : [parent.name],
);

export default function RulesPage() {
  const [sheet, setSheet] = useState<SheetState>({ open: false, keyword: "", category: "" });
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <PageTransition>
      <main className="min-h-screen bg-pf-black pb-[96px]">
        <TopBar
          title="Rules"
          back="/settings"
          right={
            <button
              type="button"
              onClick={() => setSheet({ open: true, keyword: "", category: "" })}
              className="text-[22px] font-light leading-none"
              style={{ color: PF.goldBase }}
              aria-label="Add rule"
            >
              +
            </button>
          }
        />

        <div className="px-5 py-3">
          <p className="text-[13px] leading-[1.5] text-white/45">
            When a transaction description contains the keyword, its category will be assigned
            automatically on sync. Case-insensitive substring match.
          </p>
        </div>

        <div className="mb-1 px-5">
          <span className="text-[12px] uppercase tracking-[0.3px] text-white/40">
            {MOCK_RULES.length} active rules
          </span>
        </div>

        <StaggerList>
          {MOCK_RULES.map((rule) => (
            <StaggerItem key={rule.id} className="list-none">
              <RuleRow
                rule={rule}
                open={openId === rule.id}
                onToggle={() =>
                  setOpenId((prev) => (prev === rule.id ? null : rule.id))
                }
              />
            </StaggerItem>
          ))}
        </StaggerList>

        <AnimatePresence>
          {sheet.open ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="pf-safe-bottom fixed inset-0 z-[60] flex items-end bg-black/50"
              onClick={() => setSheet((s) => ({ ...s, open: false }))}
            >
              <motion.div
                initial={{ y: 300 }}
                animate={{ y: 0 }}
                exit={{ y: 300 }}
                transition={{ duration: 0.22, ease: "easeOut" }}
                onClick={(e) => e.stopPropagation()}
                className="w-full rounded-t-[20px] border border-white/[0.08] bg-pf-near-black p-5"
              >
                <div className="mx-auto mb-4 h-1 w-10 rounded-full bg-white/20" />
                <h3 className="mb-4 text-[17px] font-semibold text-pf-white">Add rule</h3>

                <label className="mb-1 block text-[12px] text-white/45">Keyword</label>
                <input
                  autoFocus
                  value={sheet.keyword}
                  onChange={(e) => setSheet((s) => ({ ...s, keyword: e.target.value }))}
                  placeholder="e.g. amazon"
                  className="mb-4 w-full rounded-[10px] border border-white/[0.08] bg-white/[0.04] px-3 py-2.5 text-[15px] text-pf-white outline-none placeholder:text-white/30"
                />

                <label className="mb-1 block text-[12px] text-white/45">Category</label>
                <select
                  value={sheet.category}
                  onChange={(e) => setSheet((s) => ({ ...s, category: e.target.value }))}
                  className="mb-6 w-full rounded-[10px] border border-white/[0.08] bg-white/[0.04] px-3 py-2.5 text-[15px] text-pf-white outline-none"
                >
                  <option value="">— pick a category —</option>
                  {CATEGORY_OPTIONS.map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
                </select>

                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => setSheet((s) => ({ ...s, open: false }))}
                    className="flex h-12 flex-1 items-center justify-center rounded-[12px] border border-white/[0.1] text-[15px] text-pf-white"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={() => setSheet((s) => ({ ...s, open: false }))}
                    className="flex h-12 flex-1 items-center justify-center rounded-[12px] bg-gold-metallic text-[15px] font-semibold text-pf-black"
                  >
                    Add
                  </button>
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

function RuleRow({
  rule,
  open,
  onToggle,
}: {
  rule: { id: string; keyword: string; category: string };
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <div>
      <button
        type="button"
        onClick={onToggle}
        className="flex w-full items-center justify-between border-b border-white/[0.06] px-5 py-3 text-left active:bg-white/[0.02]"
      >
        <div className="min-w-0 flex-1 pr-3">
          <div className="truncate text-[15px] font-medium text-pf-white">{rule.keyword}</div>
          <div className="truncate text-[12px] text-white/45">→ {rule.category}</div>
        </div>
        <div className="flex-shrink-0 text-[11px] uppercase tracking-[0.3px] text-white/35">
          {open ? "tap to close" : "tap to edit"}
        </div>
      </button>
      <AnimatePresence>
        {open ? (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="overflow-hidden border-b border-white/[0.06] bg-white/[0.02]"
          >
            <div className="flex justify-end gap-4 px-5 py-2">
              <button
                type="button"
                className="text-[13px] font-medium"
                style={{ color: PF.goldBase }}
              >
                Edit
              </button>
              <button
                type="button"
                className="text-[13px] font-medium"
                style={{ color: PF.expense }}
              >
                Delete
              </button>
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  );
}
