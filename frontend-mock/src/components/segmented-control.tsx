"use client";

import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

type Option<T extends string> = { value: T; label: string };

type Props<T extends string> = {
  options: readonly Option<T>[];
  value: T;
  onChange: (v: T) => void;
};

export function SegmentedControl<T extends string>({
  options,
  value,
  onChange,
}: Props<T>) {
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const trackBg = dark ? "#1A1A1A" : "#EDEDED";
  const activeBg = dark ? "#2A2A2A" : "#FFFFFF";

  return (
    <div
      className="flex w-full gap-0.5 rounded-[10px] p-0.5"
      style={{ background: trackBg }}
    >
      {options.map((opt) => {
        const on = opt.value === value;
        return (
          <button
            key={opt.value}
            type="button"
            onClick={() => onChange(opt.value)}
            className="h-9 flex-1 rounded-[8px] text-[14px] font-medium transition"
            style={{
              background: on ? activeBg : "transparent",
              color: on ? C.text : C.muted,
              boxShadow: on ? "0 1px 3px rgba(0,0,0,0.08)" : "none",
            }}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
