"use client";

import { useState, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import {
  MOCK_MERCHANT_AVG,
  MOCK_MERCHANT_HISTORY,
  MOCK_TRANSACTIONS,
} from "@/lib/mock";
import { PF, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { MerchantAvatar } from "@/components/merchant-avatar";

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

export default function TransactionDetailPage() {
  const tx = MOCK_TRANSACTIONS[0]!; // Bolt Food · −€18.90
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const [note, setNote] = useState("");
  const [editNote, setEditNote] = useState(false);

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
            Transaction
          </span>
          <button
            type="button"
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

        {/* Amount hero */}
        <section
          className="px-5 pb-7 pt-6 text-center"
          style={{ borderBottom: `1px solid ${C.border}` }}
        >
          <div className="mb-4">
            <MerchantAvatar />
          </div>
          <div
            className="text-[44px] font-bold leading-none tracking-[-1.5px] tabular-nums"
            style={{ color: tx.expense ? PF.expense : PF.income }}
          >
            {tx.amount}
          </div>
          <div
            className="mt-2.5 text-[19px] font-medium"
            style={{ color: C.text }}
          >
            {tx.desc}
          </div>
          <div className="mt-1.5 text-[13px]" style={{ color: C.muted }}>
            21 Apr 2026 · 09:23 · Revolut
          </div>
        </section>

        {/* Detail rows */}
        <div className="mt-2">
          <Row label="Category" dark={dark}>
            <div className="flex items-center gap-2">
              <span
                className="rounded-full px-2.5 py-[3px] text-[14px]"
                style={{
                  background: dark ? "#2A2A2A" : "#F0F0F0",
                  color: C.text,
                }}
              >
                {tx.cat}
              </span>
              <button
                type="button"
                className="text-[13px]"
                style={{ color: PF.goldBase }}
              >
                Edit
              </button>
            </div>
          </Row>

          <Row label="Account" dark={dark}>
            <div className="flex items-center gap-1.5">
              <span
                className="flex h-5 w-5 items-center justify-center rounded-[5px] text-[9px] font-bold text-white"
                style={{ background: "#191C1F" }}
              >
                R
              </span>
              <span className="text-[15px]" style={{ color: C.text }}>
                Revolut
              </span>
            </div>
          </Row>

          <Row label="Date & time" dark={dark}>
            <span className="text-[15px]" style={{ color: C.text }}>
              21 Apr 2026, 09:23
            </span>
          </Row>

          <Row label="Currency" dark={dark}>
            <span className="text-[15px]" style={{ color: C.text }}>
              EUR
            </span>
          </Row>

          <div
            className="px-5 py-3"
            style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
          >
            <div
              className="flex items-center justify-between"
              style={{ marginBottom: editNote || note ? 8 : 0 }}
            >
              <span className="text-[15px]" style={{ color: C.muted }}>
                Note
              </span>
              <button
                type="button"
                onClick={() => setEditNote((e) => !e)}
                className="text-[13px]"
                style={{ color: PF.goldBase }}
              >
                {editNote ? "Done" : note ? "Edit" : "Add"}
              </button>
            </div>
            {editNote ? (
              <textarea
                autoFocus
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="e.g. team lunch, reimbursable"
                className="min-h-[56px] w-full resize-none rounded-[8px] p-2.5 text-[14px] leading-[1.5] outline-none"
                style={{
                  background: C.surface,
                  border: `1px solid ${C.border}`,
                  color: C.text,
                }}
              />
            ) : note ? (
              <div
                className="text-[14px] leading-[1.5]"
                style={{ color: C.text }}
              >
                {note}
              </div>
            ) : null}
          </div>
        </div>

        {/* Merchant history */}
        <section className="mt-5">
          <div className="flex items-center justify-between px-5 pb-2.5">
            <span
              className="text-[15px] font-semibold"
              style={{ color: C.text }}
            >
              Bolt Food · history
            </span>
            <span className="text-[13px]" style={{ color: C.muted }}>
              last 3
            </span>
          </div>
          {MOCK_MERCHANT_HISTORY.map((h) => (
            <div
              key={h.date}
              className="flex h-12 items-center justify-between px-5"
              style={{ borderTop: `1px solid ${C.subtleBorder}` }}
            >
              <span className="text-[14px]" style={{ color: C.muted }}>
                {h.date}
              </span>
              <span
                className="text-[14px] font-medium tabular-nums"
                style={{ color: PF.expense }}
              >
                {h.amount}
              </span>
            </div>
          ))}
          <div
            className="mx-5 mt-3 flex items-center justify-between rounded-[10px] px-3.5 py-2.5"
            style={{
              background: dark ? "#1A1A1A" : "#F7F7F7",
              border: `1px solid ${C.border}`,
            }}
          >
            <span className="text-[13px]" style={{ color: C.muted }}>
              Avg charge · last 3 months
            </span>
            <span
              className="text-[14px] font-semibold tabular-nums"
              style={{ color: C.text }}
            >
              {MOCK_MERCHANT_AVG}
            </span>
          </div>
        </section>
      </main>
    </PageTransition>
  );
}

function Row({
  label,
  dark,
  children,
}: {
  label: string;
  dark: boolean;
  children: ReactNode;
}) {
  const C = pfTheme(dark);
  return (
    <div
      className="flex min-h-[52px] items-center justify-between px-5"
      style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
    >
      <span
        className="flex-shrink-0 text-[15px]"
        style={{ color: C.muted }}
      >
        {label}
      </span>
      <div className="text-right">{children}</div>
    </div>
  );
}
