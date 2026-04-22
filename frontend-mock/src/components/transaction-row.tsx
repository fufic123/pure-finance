"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { MockTransaction } from "@/lib/mock";
import { PF, pfTheme } from "@/lib/tokens";
import { staggerItem } from "@/components/stagger-list";

type Props = {
  tx: MockTransaction;
  href?: string;
  dark?: boolean;
};

export function TransactionRow({ tx, href = `/transactions/${tx.id}`, dark = false }: Props) {
  const C = pfTheme(dark);

  return (
    <motion.li variants={staggerItem} className="list-none">
      <Link
        href={href}
        className="flex h-[62px] items-center gap-3 px-5"
        style={{
          borderBottom: `1px solid ${C.subtleBorder}`,
          background: C.bg,
        }}
      >
        <div className="w-7 flex-shrink-0 text-center">
          <div className="text-[17px] font-semibold leading-none" style={{ color: C.text }}>
            {tx.day}
          </div>
          <div className="mt-[3px] text-[11px]" style={{ color: C.muted }}>
            {tx.mon}
          </div>
        </div>
        <div className="min-w-0 flex-1">
          <div className="truncate text-[15px]" style={{ color: C.text }}>
            {tx.desc}
          </div>
          {tx.cat ? (
            <div className="mt-[3px]">
              <span
                className="inline-block rounded-full px-2 py-[1px] text-[11px]"
                style={{
                  background: dark ? "#2A2A2A" : "#F0F0F0",
                  color: C.muted,
                }}
              >
                {tx.cat}
              </span>
            </div>
          ) : null}
        </div>
        <div
          className="flex-shrink-0 text-[15px] font-medium tabular-nums"
          style={{ color: tx.expense ? PF.expense : PF.income }}
        >
          {tx.amount}
        </div>
      </Link>
    </motion.li>
  );
}
