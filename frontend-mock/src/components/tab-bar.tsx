"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import type { ReactElement } from "react";
import { GOLD_TEXT_STYLE, PF } from "@/lib/tokens";

type TabId = "home" | "transactions" | "analytics" | "settings";

type Tab = {
  id: TabId;
  label: string;
  href: "/home" | "/transactions" | "/analytics" | "/settings";
  Icon: (props: { color: string }) => ReactElement;
};

function IcHome({ color }: { color: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}
function IcList({ color }: { color: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.6"
      strokeLinecap="round"
    >
      <line x1="8" y1="6" x2="21" y2="6" />
      <line x1="8" y1="12" x2="21" y2="12" />
      <line x1="8" y1="18" x2="21" y2="18" />
      <line x1="3" y1="6" x2="3.01" y2="6" />
      <line x1="3" y1="12" x2="3.01" y2="12" />
      <line x1="3" y1="18" x2="3.01" y2="18" />
    </svg>
  );
}
function IcChart({ color }: { color: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="9" />
      <path d="M12 12L12 3M12 12L19.5 7.5" />
    </svg>
  );
}
function IcPerson({ color }: { color: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="8" r="4" />
      <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
    </svg>
  );
}

const TABS: Tab[] = [
  { id: "home", label: "Home", href: "/home", Icon: IcHome },
  { id: "transactions", label: "Transactions", href: "/transactions", Icon: IcList },
  { id: "analytics", label: "Analytics", href: "/analytics", Icon: IcChart },
  { id: "settings", label: "Settings", href: "/settings", Icon: IcPerson },
];

export function TabBar() {
  const pathname = usePathname();
  const active: TabId =
    pathname.startsWith("/transactions")
      ? "transactions"
      : pathname.startsWith("/analytics")
        ? "analytics"
        : pathname.startsWith("/settings")
          ? "settings"
          : "home";

  return (
    <nav
      className="pf-safe-bottom fixed bottom-0 left-0 right-0 z-50 bg-pf-black/90 backdrop-blur"
      style={{ borderTop: "1px solid #1F1F1F" }}
    >
      <ul className="flex h-[64px] items-start pt-[10px]">
        {TABS.map((t) => {
          const on = t.id === active;
          const color = on ? PF.goldBase : "rgba(255,255,255,0.4)";
          return (
            <li key={t.id} className="flex-1">
              <Link href={t.href} className="flex flex-col items-center gap-1">
                <motion.div
                  animate={{ color }}
                  transition={{ duration: 0.15, ease: "easeOut" }}
                  style={{ color }}
                  whileTap={{ scale: 0.92 }}
                >
                  <t.Icon color={color} />
                </motion.div>
                <span
                  className="text-[10px] tracking-[0.2px]"
                  style={
                    on
                      ? { ...GOLD_TEXT_STYLE, fontWeight: 600 }
                      : { color: "rgba(255,255,255,0.4)", fontWeight: 400 }
                  }
                >
                  {t.label}
                </span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
