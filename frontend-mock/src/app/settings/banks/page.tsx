"use client";

import Link from "next/link";
import { MOCK_CONNECTIONS, type ConnectionStatus } from "@/lib/mock";
import { GRAD_METALLIC, PF, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { TopBar } from "@/components/top-bar";
import { PageTransition } from "@/components/page-transition";
import { StaggerItem, StaggerList } from "@/components/stagger-list";
import { TabBar } from "@/components/tab-bar";

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

function statusColor(status: ConnectionStatus): { bg: string; fg: string; label: string } {
  switch (status) {
    case "COMPLETED":
      return { bg: "rgba(31,122,61,0.18)", fg: PF.income, label: "Connected" };
    case "CREATED":
      return { bg: "rgba(168,116,0,0.18)", fg: PF.warning, label: "Pending" };
    case "EXPIRED":
      return { bg: "rgba(176,58,46,0.18)", fg: PF.expense, label: "Expired" };
    case "REVOKED":
      return { bg: "rgba(107,107,107,0.18)", fg: "#999999", label: "Revoked" };
  }
}

export default function BanksPage() {
  const { dark } = useTheme();
  const C = pfTheme(dark);

  return (
    <PageTransition>
      <main
        className="min-h-screen pb-[96px]"
        style={{ background: C.bg }}
      >
        <TopBar title="Banks" back />

        <div className="px-5 py-3">
          <Link
            href="/onboarding"
            className="flex h-[52px] items-center justify-center gap-2 rounded-[14px] text-[15px] font-semibold active:opacity-90"
            style={{ background: GRAD_METALLIC, color: "#0A0A0A" }}
          >
            + Add bank
          </Link>
        </div>

        <div className="mb-1 px-5">
          <span
            className="text-[12px] uppercase tracking-[0.3px]"
            style={{ color: C.muted }}
          >
            Connected
          </span>
        </div>

        <StaggerList>
          {MOCK_CONNECTIONS.map((conn) => {
            const s = statusColor(conn.status);
            return (
              <StaggerItem key={conn.id} className="list-none">
                <button
                  type="button"
                  className="flex w-full items-center gap-3.5 px-5 py-3 text-left"
                  style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
                >
                  <div
                    className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-[10px] text-[14px] font-bold text-white"
                    style={{ background: conn.bank.color }}
                  >
                    {conn.bank.abbr}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span
                        className="truncate text-[15px] font-medium"
                        style={{ color: C.text }}
                      >
                        {conn.bank.name}
                      </span>
                      <span
                        className="rounded-full px-1.5 py-[2px] text-[10px] font-medium uppercase tracking-[0.3px]"
                        style={{ background: s.bg, color: s.fg }}
                      >
                        {s.label}
                      </span>
                    </div>
                    <div className="text-[12px]" style={{ color: C.muted }}>
                      Added {conn.created}
                    </div>
                  </div>
                  <ChevronRight color={C.muted} />
                </button>
              </StaggerItem>
            );
          })}
        </StaggerList>

        <TabBar />
      </main>
    </PageTransition>
  );
}
