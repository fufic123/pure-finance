"use client";

import Link from "next/link";
import type { ReactNode } from "react";

type Props = {
  title?: string;
  left?: ReactNode;
  right?: ReactNode;
  back?: string;
  backLabel?: string;
};

function ChevronLeft() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d="M15 18l-6-6 6-6" />
    </svg>
  );
}

export function TopBar({ title, left, right, back, backLabel = "Back" }: Props) {
  return (
    <div className="pf-safe-top sticky top-0 z-40 bg-pf-black/85 backdrop-blur">
      <div className="flex h-[52px] items-center justify-between px-5">
        <div className="flex min-w-[64px] items-center gap-1 text-white/45">
          {back ? (
            <Link href={back} className="flex items-center gap-1 text-[15px]">
              <ChevronLeft />
              <span>{backLabel}</span>
            </Link>
          ) : (
            left
          )}
        </div>
        {title ? (
          <span className="truncate text-[17px] font-semibold tracking-tight text-pf-white">
            {title}
          </span>
        ) : (
          <span />
        )}
        <div className="flex min-w-[64px] items-center justify-end gap-2">{right}</div>
      </div>
    </div>
  );
}
