"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { MOCK_CATEGORY_TREE, type CategoryNode } from "@/lib/mock";
import { PF } from "@/lib/tokens";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";

type AddSheetState = {
  open: boolean;
  name: string;
  parent: string;
};

export default function CategoriesPage() {
  const [sheet, setSheet] = useState<AddSheetState>({ open: false, name: "", parent: "" });
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <PageTransition>
      <main className="min-h-screen bg-pf-black pb-[96px]">
        <TopBar
          title="Categories"
          back="/settings"
          right={
            <button
              type="button"
              onClick={() => setSheet({ open: true, name: "", parent: "" })}
              className="text-[22px] font-light leading-none"
              style={{ color: PF.goldBase }}
              aria-label="Add category"
            >
              +
            </button>
          }
        />

        <div className="px-5 py-3">
          <p className="text-[13px] leading-[1.5] text-white/45">
            Organize transactions. System categories can&apos;t be removed. Tap a user row to
            reveal Delete.
          </p>
        </div>

        {MOCK_CATEGORY_TREE.map((parent) => (
          <Section key={parent.id}>
            <Header node={parent} />
            {parent.children.length ? (
              <StaggerList>
                {parent.children.map((child) => (
                  <StaggerItem key={child.id} className="list-none">
                    <ChildRow
                      node={child}
                      open={openId === child.id}
                      onToggle={() => setOpenId((prev) => (prev === child.id ? null : child.id))}
                    />
                  </StaggerItem>
                ))}
              </StaggerList>
            ) : null}
          </Section>
        ))}

        {/* Add sheet — inline */}
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
                <h3 className="mb-4 text-[17px] font-semibold text-pf-white">Add category</h3>
                <label className="mb-1 block text-[12px] text-white/45">Name</label>
                <input
                  autoFocus
                  value={sheet.name}
                  onChange={(e) => setSheet((s) => ({ ...s, name: e.target.value }))}
                  placeholder="e.g. Pharmacy"
                  className="mb-4 w-full rounded-[10px] border border-white/[0.08] bg-white/[0.04] px-3 py-2.5 text-[15px] text-pf-white outline-none placeholder:text-white/30"
                />
                <label className="mb-1 block text-[12px] text-white/45">Parent (optional)</label>
                <select
                  value={sheet.parent}
                  onChange={(e) => setSheet((s) => ({ ...s, parent: e.target.value }))}
                  className="mb-6 w-full rounded-[10px] border border-white/[0.08] bg-white/[0.04] px-3 py-2.5 text-[15px] text-pf-white outline-none"
                >
                  <option value="">— none —</option>
                  {MOCK_CATEGORY_TREE.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
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

function Section({ children }: { children: React.ReactNode }) {
  return <section className="mb-2">{children}</section>;
}

function Header({ node }: { node: CategoryNode }) {
  return (
    <div className="flex items-center justify-between border-b border-white/[0.08] px-5 py-2.5">
      <span className="text-[13px] font-semibold uppercase tracking-[0.4px] text-white/55">
        {node.name}
      </span>
      {node.system ? (
        <span className="rounded-full bg-white/[0.06] px-2 py-[2px] text-[10px] uppercase tracking-[0.3px] text-white/45">
          system
        </span>
      ) : null}
    </div>
  );
}

function ChildRow({
  node,
  open,
  onToggle,
}: {
  node: CategoryNode;
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <div>
      <button
        type="button"
        onClick={onToggle}
        className="flex h-12 w-full items-center justify-between border-b border-white/[0.06] pl-8 pr-5 text-left active:bg-white/[0.02]"
      >
        <span className="text-[15px] text-pf-white">{node.name}</span>
        {node.system ? (
          <span className="text-[11px] uppercase tracking-[0.3px] text-white/35">system</span>
        ) : null}
      </button>
      <AnimatePresence>
        {open && !node.system ? (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="overflow-hidden border-b border-white/[0.06] bg-white/[0.02]"
          >
            <div className="flex justify-end px-5 py-2">
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
