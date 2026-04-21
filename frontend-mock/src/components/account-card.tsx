"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { MockAccount } from "@/lib/mock";
import { staggerItem } from "@/components/stagger-list";

type Props = { account: MockAccount };

export function AccountCard({ account }: Props) {
  return (
    <motion.li variants={staggerItem} className="list-none">
      <Link
        href={`/accounts/${account.id}`}
        className="flex h-[60px] items-center gap-3.5 border-b border-white/[0.06] px-5 active:bg-white/[0.02]"
      >
        <div
          className="flex h-[34px] w-[34px] flex-shrink-0 items-center justify-center rounded-[9px] text-[13px] font-bold text-white"
          style={{ background: account.color }}
        >
          {account.logo}
        </div>
        <div className="flex-1">
          <div className="text-[15px] font-medium text-pf-white">{account.name}</div>
          <div className="text-[12px] text-white/40">{account.currency}</div>
        </div>
        <div className="text-[16px] font-semibold tabular-nums text-pf-white">
          €{account.balance}
        </div>
      </Link>
    </motion.li>
  );
}
