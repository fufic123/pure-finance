"use client";

import { useState } from "react";
import { MOCK_TRANSACTIONS } from "@/lib/mock";
import { PF } from "@/lib/tokens";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import type { ReactNode } from "react";

export default function TransactionDetailPage() {
  const tx = MOCK_TRANSACTIONS[0]!; // first (Bolt Food) — mock detail target
  const [note, setNote] = useState("");
  const [editNote, setEditNote] = useState(false);

  const merchantHistory = [
    { date: "Apr 14", amount: "−€14.60" },
    { date: "Apr 7", amount: "−€22.10" },
    { date: "Mar 31", amount: "−€17.50" },
  ];

  return (
    <PageTransition>
      <main className="min-h-screen bg-pf-black pb-20">
        <TopBar title="Transaction" back="/transactions" />

        {/* Amount hero */}
        <section className="border-b border-white/[0.08] px-5 pb-7 pt-6 text-center">
          <div
            className="mx-auto mb-4 flex h-[52px] w-[52px] items-center justify-center rounded-[14px] text-[22px]"
            style={{ background: "#191C1F" }}
          >
            <span aria-hidden>{"\u{1F6F5}"}</span>
          </div>
          <div
            className="text-[44px] font-bold leading-none tracking-[-1.5px] tabular-nums"
            style={{ color: tx.expense ? PF.expense : PF.income }}
          >
            {tx.amount}
          </div>
          <div className="mt-2.5 text-[19px] font-medium text-pf-white">{tx.desc}</div>
          <div className="mt-1.5 text-[13px] text-white/45">
            21 Apr 2026 · 09:23 · Revolut
          </div>
        </section>

        {/* Detail rows */}
        <div className="mt-2">
          <Row label="Category">
            <div className="flex items-center gap-2">
              <span className="rounded-full bg-white/[0.08] px-2.5 py-[3px] text-[14px] text-pf-white">
                {tx.cat}
              </span>
              <button type="button" className="text-[13px]" style={{ color: PF.goldBase }}>
                Edit
              </button>
            </div>
          </Row>

          <Row label="Account">
            <div className="flex items-center gap-1.5">
              <span
                className="flex h-5 w-5 items-center justify-center rounded-[5px] text-[9px] font-bold text-white"
                style={{ background: "#191C1F" }}
              >
                R
              </span>
              <span className="text-[15px] text-pf-white">Revolut</span>
            </div>
          </Row>

          <Row label="Date & time">
            <span className="text-[15px] text-pf-white">21 Apr 2026, 09:23</span>
          </Row>

          <Row label="Currency">
            <span className="text-[15px] text-pf-white">EUR</span>
          </Row>

          <div className="border-b border-white/[0.06] px-5 py-3">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-[15px] text-white/45">Note</span>
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
                className="min-h-[56px] w-full resize-none rounded-[8px] border border-white/[0.08] bg-white/[0.04] p-2.5 text-[14px] leading-[1.5] text-pf-white outline-none placeholder:text-white/30"
              />
            ) : note ? (
              <div className="text-[14px] leading-[1.5] text-pf-white">{note}</div>
            ) : null}
          </div>
        </div>

        {/* Merchant history */}
        <section className="mt-5">
          <div className="flex items-center justify-between px-5 pb-2.5">
            <span className="text-[15px] font-semibold text-pf-white">Bolt Food · history</span>
            <span className="text-[13px] text-white/40">last 3</span>
          </div>
          {merchantHistory.map((h) => (
            <div
              key={h.date}
              className="flex h-12 items-center justify-between border-t border-white/[0.06] px-5"
            >
              <span className="text-[14px] text-white/45">{h.date}</span>
              <span
                className="text-[14px] font-medium tabular-nums"
                style={{ color: PF.expense }}
              >
                {h.amount}
              </span>
            </div>
          ))}
          <div className="mx-5 mt-3 flex items-center justify-between rounded-[10px] border border-white/[0.08] bg-white/[0.04] px-3.5 py-2.5">
            <span className="text-[13px] text-white/45">Avg charge · last 3 months</span>
            <span className="text-[14px] font-semibold tabular-nums text-pf-white">−€18.30</span>
          </div>
        </section>
      </main>
    </PageTransition>
  );
}

function Row({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex min-h-[52px] items-center justify-between border-b border-white/[0.06] px-5">
      <span className="flex-shrink-0 text-[15px] text-white/45">{label}</span>
      <div className="text-right">{children}</div>
    </div>
  );
}
