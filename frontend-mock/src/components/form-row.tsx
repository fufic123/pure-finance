"use client";

import type { ReactNode } from "react";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

type Props = {
  label: string;
  onClick?: () => void;
  chevron?: boolean;
  children: ReactNode;
};

export function FormRow({ label, onClick, chevron = false, children }: Props) {
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const clickable = typeof onClick === "function";

  return (
    <div
      role={clickable ? "button" : undefined}
      tabIndex={clickable ? 0 : undefined}
      onClick={onClick}
      onKeyDown={
        clickable
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
      className="flex min-h-[52px] items-center justify-between px-4"
      style={{
        borderBottom: `1px solid ${C.subtleBorder}`,
        cursor: clickable ? "pointer" : "default",
      }}
    >
      <span className="text-[15px]" style={{ color: C.muted }}>
        {label}
      </span>
      <div className="flex items-center gap-2 text-right">
        <div className="text-[15px]" style={{ color: C.text }}>
          {children}
        </div>
        {chevron ? (
          <span style={{ color: C.muted, fontSize: 18 }}>›</span>
        ) : null}
      </div>
    </div>
  );
}
