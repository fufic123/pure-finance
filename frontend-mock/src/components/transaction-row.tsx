"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { MockTransaction } from "@/lib/mock";
import { staggerItem } from "@/components/stagger-list";

type Props = {
  tx: MockTransaction;
  href?: string;
};

export function TransactionRow({ tx, href = `/transactions/${tx.id}` }: Props) {
  return (
    <motion.li variants={staggerItem} className="list-none">
      <Link
        href={href}
        className="flex h-[62px] items-center gap-3 border-b border-white/[0.06] px-5 active:bg-white/[0.02]"
      >
        <div className="w-7 flex-shrink-0 text-center">
          <div className="text-[17px] font-semibold leading-none text-pf-white">{tx.day}</div>
          <div className="mt-[3px] text-[11px] text-white/40">{tx.mon}</div>
        </div>
        <div className="min-w-0 flex-1">
          <div className="truncate text-[15px] text-pf-white">{tx.desc}</div>
          {tx.cat ? (
            <div className="mt-[3px]">
              <span className="inline-block rounded-full bg-white/[0.08] px-2 py-[1px] text-[11px] text-white/50">
                {tx.cat}
              </span>
            </div>
          ) : null}
        </div>
        <div
          className="flex-shrink-0 text-[15px] font-medium tabular-nums"
          style={{ color: tx.expense ? "#B03A2E" : "#1F7A3D" }}
        >
          {tx.amount}
        </div>
      </Link>
    </motion.li>
  );
}
