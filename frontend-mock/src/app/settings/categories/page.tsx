"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";
import { MOCK_CATEGORY_TREE, type CategoryNode } from "@/lib/mock";
import { GRAD_METALLIC, PF, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
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
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const [sheet, setSheet] = useState<AddSheetState>({ open: false, name: "", parent: "" });
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <PageTransition>
      <main className="min-h-screen pb-[96px]" style={{ background: C.bg }}>
        <TopBar
          title="Categories"
          back
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
          <p
            className="text-[13px] leading-[1.5]"
            style={{ color: C.muted }}
          >
            Organize transactions. System categories can&apos;t be edited or removed. Tap a user row to reveal Edit and Delete.
          </p>
        </div>

        {MOCK_CATEGORY_TREE.map((parent) => (
          <section key={parent.id} className="mb-2">
            <Header node={parent} dark={dark} />
            {parent.children.length ? (
              <StaggerList>
                {parent.children.map((child) => (
                  <StaggerItem key={child.id} className="list-none">
                    <ChildRow
                      node={child}
                      dark={dark}
                      open={openId === child.id}
                      onToggle={() =>
                        setOpenId((prev) => (prev === child.id ? null : child.id))
                      }
                    />
                  </StaggerItem>
                ))}
              </StaggerList>
            ) : null}
          </section>
        ))}

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
                  Add category
                </h3>
                <label className="mb-1 block text-[12px]" style={{ color: C.muted }}>
                  Name
                </label>
                <input
                  autoFocus
                  value={sheet.name}
                  onChange={(e) => setSheet((s) => ({ ...s, name: e.target.value }))}
                  placeholder="e.g. Pharmacy"
                  className="mb-4 w-full rounded-[10px] px-3 py-2.5 text-[15px] outline-none"
                  style={{
                    background: C.surface,
                    border: `1px solid ${C.border}`,
                    color: C.text,
                  }}
                />
                <label className="mb-1 block text-[12px]" style={{ color: C.muted }}>
                  Parent (optional)
                </label>
                <select
                  value={sheet.parent}
                  onChange={(e) => setSheet((s) => ({ ...s, parent: e.target.value }))}
                  className="mb-6 w-full rounded-[10px] px-3 py-2.5 text-[15px] outline-none"
                  style={{
                    background: C.surface,
                    border: `1px solid ${C.border}`,
                    color: C.text,
                  }}
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

function Header({ node, dark }: { node: CategoryNode; dark: boolean }) {
  const C = pfTheme(dark);
  return (
    <div
      className="flex items-center justify-between px-5 py-2.5"
      style={{ borderBottom: `1px solid ${C.border}` }}
    >
      <span
        className="text-[13px] font-semibold uppercase tracking-[0.4px]"
        style={{ color: C.muted }}
      >
        {node.name}
      </span>
      {node.system ? (
        <span
          className="rounded-full px-2 py-[2px] text-[10px] uppercase tracking-[0.3px]"
          style={{
            background: dark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)",
            color: C.muted,
          }}
        >
          system
        </span>
      ) : null}
    </div>
  );
}

function ChildRow({
  node,
  dark,
  open,
  onToggle,
}: {
  node: CategoryNode;
  dark: boolean;
  open: boolean;
  onToggle: () => void;
}) {
  const C = pfTheme(dark);
  const router = useRouter();
  return (
    <div>
      <button
        type="button"
        onClick={onToggle}
        className="flex h-12 w-full items-center justify-between pl-8 pr-5 text-left"
        style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
      >
        <span className="text-[15px]" style={{ color: C.text }}>
          {node.name}
        </span>
        {node.system ? (
          <span
            className="text-[11px] uppercase tracking-[0.3px]"
            style={{ color: C.muted }}
          >
            system
          </span>
        ) : null}
      </button>
      <AnimatePresence>
        {open && !node.system ? (
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
                onClick={() => router.push(`/settings/categories/${node.id}/edit`)}
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
