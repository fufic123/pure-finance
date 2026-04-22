"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { MockAccount } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { staggerItem } from "@/components/stagger-list";

type Props = { account: MockAccount; dark?: boolean };

export function AccountCard({ account, dark = false }: Props) {
  const C = pfTheme(dark);
  return (
    <motion.li variants={staggerItem} className="list-none">
      <Link
        href={`/accounts/${account.id}`}
        className="flex h-[60px] items-center gap-3.5 px-5"
        style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
      >
        <div
          className="flex h-[34px] w-[34px] flex-shrink-0 items-center justify-center rounded-[9px] text-[13px] font-bold text-white"
          style={{ background: account.color }}
        >
          {account.logo}
        </div>
        <div className="flex-1">
          <div className="text-[15px] font-medium" style={{ color: C.text }}>
            {account.name}
          </div>
          <div className="text-[12px]" style={{ color: C.muted }}>
            {account.currency}
          </div>
        </div>
        <div className="text-[16px] font-semibold tabular-nums" style={{ color: C.text }}>
          €{account.balance}
        </div>
      </Link>
    </motion.li>
  );
}
