"use client";

import Link from "next/link";
import { MOCK_BANKS } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";

function ChevronRight({ color }: { color: string }) {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M9 18l6-6-6-6" />
    </svg>
  );
}

function ChevronDown({ color }: { color: string }) {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 9l6 6 6-6" />
    </svg>
  );
}

export default function OnboardingPage() {
  const { dark } = useTheme();
  const C = pfTheme(dark);

  return (
    <PageTransition>
      <main className="min-h-screen" style={{ background: C.bg }}>
        <TopBar title="Connect a bank" back />

        <div
          className="px-5 py-5"
          style={{ borderBottom: `1px solid ${C.border}` }}
        >
          <p
            className="m-0 text-[14px]"
            style={{ color: C.muted, lineHeight: 1.55 }}
          >
            We read your transactions through GoCardless (PSD2). Pure Finance never sees your
            password — you authorize directly with the bank.
          </p>
        </div>

        <div
          className="flex h-[52px] items-center justify-between px-5"
          style={{ borderBottom: `1px solid ${C.border}` }}
        >
          <span className="text-[15px]" style={{ color: C.text }}>
            Country
          </span>
          <div className="flex items-center gap-1.5" style={{ color: C.muted }}>
            <span className="text-[15px]">Lithuania</span>
            <ChevronDown color={C.muted} />
          </div>
        </div>

        <StaggerList className="py-2">
          {MOCK_BANKS.map((bank) => (
            <StaggerItem key={bank.id} className="list-none">
              <Link
                href="/home"
                className="flex h-16 items-center gap-3.5 px-5"
                style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
              >
                <div
                  className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-[10px] text-[14px] font-bold text-white"
                  style={{ background: bank.color }}
                >
                  {bank.abbr}
                </div>
                <span
                  className="flex-1 text-[16px]"
                  style={{ color: C.text }}
                >
                  {bank.name}
                </span>
                <ChevronRight color={C.muted} />
              </Link>
            </StaggerItem>
          ))}
        </StaggerList>
      </main>
    </PageTransition>
  );
}
