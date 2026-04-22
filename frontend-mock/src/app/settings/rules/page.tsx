"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { MOCK_RULES, MOCK_CATEGORY_TREE } from "@/lib/mock";
import { GRAD_METALLIC, PF, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";

type SheetState = {
  open: boolean;
  keyword: string;
  category: string;
};

const CATEGORY_OPTIONS: string[] = MOCK_CATEGORY_TREE.flatMap((parent) =>
  parent.children.length
    ? parent.children.map((child) => `${parent.name} · ${child.name}`)
    : [parent.name],
);

export default function RulesPage() {
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const [sheet, setSheet] = useState<SheetState>({ open: false, keyword: "", category: "" });
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <PageTransition>
      <main
        className="min-h-screen pb-[96px]"
        style={{ background: C.bg }}
      >
        <TopBar
          title="Rules"
          back
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
          <p
            className="text-[13px] leading-[1.5]"
            style={{ color: C.muted }}
          >
            When a transaction description contains the keyword, its category will be assigned
            automatically on sync. Case-insensitive substring match.
          </p>
        </div>

        <div className="mb-1 px-5">
          <span
            className="text-[12px] uppercase tracking-[0.3px]"
            style={{ color: C.muted }}
          >
            {MOCK_RULES.length} active rules
          </span>
        </div>

        <StaggerList>
          {MOCK_RULES.map((rule) => (
            <StaggerItem key={rule.id} className="list-none">
              <RuleRow
                rule={rule}
                dark={dark}
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
                className="w-full rounded-t-[20px] p-5"
                style={{
                  background: dark ? "#1A1A1A" : "#FFFFFF",
                  border: `1px solid ${C.border}`,
                }}
              >
                <div
                  className="mx-auto mb-4 h-1 w-10 rounded-full"
                  style={{ background: C.border }}
                />
                <h3
                  className="mb-4 text-[17px] font-semibold"
                  style={{ color: C.text }}
                >
                  Add rule
                </h3>

                <label className="mb-1 block text-[12px]" style={{ color: C.muted }}>
                  Keyword
                </label>
                <input
                  autoFocus
                  value={sheet.keyword}
                  onChange={(e) => setSheet((s) => ({ ...s, keyword: e.target.value }))}
                  placeholder="e.g. amazon"
                  className="mb-4 w-full rounded-[10px] px-3 py-2.5 text-[15px] outline-none"
                  style={{
                    background: C.surface,
                    border: `1px solid ${C.border}`,
                    color: C.text,
                  }}
                />

                <label className="mb-1 block text-[12px]" style={{ color: C.muted }}>
                  Category
                </label>
                <select
                  value={sheet.category}
                  onChange={(e) => setSheet((s) => ({ ...s, category: e.target.value }))}
                  className="mb-6 w-full rounded-[10px] px-3 py-2.5 text-[15px] outline-none"
                  style={{
                    background: C.surface,
                    border: `1px solid ${C.border}`,
                    color: C.text,
                  }}
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
                    className="flex h-12 flex-1 items-center justify-center rounded-[12px] text-[15px]"
                    style={{
                      border: `1px solid ${C.border}`,
                      color: C.text,
                    }}
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={() => setSheet((s) => ({ ...s, open: false }))}
                    className="flex h-12 flex-1 items-center justify-center rounded-[12px] text-[15px] font-semibold"
                    style={{ background: GRAD_METALLIC, color: "#0A0A0A" }}
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
  dark,
  open,
  onToggle,
}: {
  rule: { id: string; keyword: string; category: string };
  dark: boolean;
  open: boolean;
  onToggle: () => void;
}) {
  const C = pfTheme(dark);
  return (
    <div>
      <button
        type="button"
        onClick={onToggle}
        className="flex w-full items-center justify-between px-5 py-3 text-left"
        style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
      >
        <div className="min-w-0 flex-1 pr-3">
          <div
            className="truncate text-[15px] font-medium"
            style={{ color: C.text }}
          >
            {rule.keyword}
          </div>
          <div className="truncate text-[12px]" style={{ color: C.muted }}>
            → {rule.category}
          </div>
        </div>
        <div
          className="flex-shrink-0 text-[11px] uppercase tracking-[0.3px]"
          style={{ color: C.muted }}
        >
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
            className="overflow-hidden"
            style={{
              borderBottom: `1px solid ${C.subtleBorder}`,
              background: dark ? "rgba(255,255,255,0.02)" : "rgba(0,0,0,0.02)",
            }}
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
