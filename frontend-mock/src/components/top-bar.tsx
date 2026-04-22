"use client";

import { useRouter } from "next/navigation";
import type { ReactNode } from "react";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

type Props = {
  title?: string;
  left?: ReactNode;
  right?: ReactNode;
  /** When true, the back chevron calls router.back(). */
  back?: boolean;
  backLabel?: string;
};

function ChevronLeft({ color }: { color: string }) {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d="M15 18l-6-6 6-6" />
    </svg>
  );
}

export function TopBar({ title, left, right, back = false, backLabel = "Back" }: Props) {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);

  return (
    <div
      className="pf-safe-top sticky top-0 z-40 backdrop-blur"
      style={{
        background: dark ? "rgba(10,10,10,0.85)" : "rgba(255,255,255,0.85)",
      }}
    >
      <div className="flex h-[52px] items-center justify-between px-5">
        <div className="flex min-w-[64px] items-center gap-1" style={{ color: C.muted }}>
          {back ? (
            <button
              type="button"
              onClick={() => router.back()}
              className="flex items-center gap-1 text-[15px]"
            >
              <ChevronLeft color={C.muted} />
              <span>{backLabel}</span>
            </button>
          ) : (
            left
          )}
        </div>
        {title ? (
          <span
            className="truncate text-[17px] font-semibold tracking-tight"
            style={{ color: C.text }}
          >
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
