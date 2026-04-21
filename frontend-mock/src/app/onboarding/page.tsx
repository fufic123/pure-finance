"use client";

import Link from "next/link";
import { MOCK_BANKS } from "@/lib/mock";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";

function ChevronRight() {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M9 18l6-6-6-6" />
    </svg>
  );
}

function ChevronDown() {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 9l6 6 6-6" />
    </svg>
  );
}

export default function OnboardingPage() {
  return (
    <PageTransition>
      <main className="min-h-screen bg-pf-black">
        <TopBar title="Connect a bank" />
        <div className="border-b border-white/[0.08] px-5 py-5">
          <p className="text-[14px] leading-[1.55] text-white/45">
            We read your transactions through GoCardless (PSD2). Pure Finance never sees your
            password — you authorize directly with the bank.
          </p>
        </div>
        <div className="flex h-[52px] items-center justify-between border-b border-white/[0.08] px-5">
          <span className="text-[15px] text-pf-white">Country</span>
          <div className="flex items-center gap-1.5 text-white/45">
            <span className="text-[15px]">Lithuania</span>
            <ChevronDown />
          </div>
        </div>
        <StaggerList className="py-2">
          {MOCK_BANKS.map((bank) => (
            <StaggerItem key={bank.id} className="list-none">
              <Link
                href="/home"
                className="flex h-16 items-center gap-3.5 border-b border-white/[0.06] px-5 active:bg-white/[0.02]"
              >
                <div
                  className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-[10px] text-[14px] font-bold text-white"
                  style={{ background: bank.color }}
                >
                  {bank.abbr}
                </div>
                <span className="flex-1 text-[16px] text-pf-white">{bank.name}</span>
                <span className="text-white/40">
                  <ChevronRight />
                </span>
              </Link>
            </StaggerItem>
          ))}
        </StaggerList>
      </main>
    </PageTransition>
  );
}
