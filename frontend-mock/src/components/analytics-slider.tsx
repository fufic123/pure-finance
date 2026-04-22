"use client";

import { Children, useRef, useState, type ReactNode } from "react";
import { GRAD_METALLIC_SUBTLE, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

type Props = { children: ReactNode };

export function AnalyticsSlider({ children }: Props) {
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [active, setActive] = useState(0);
  const count = Children.count(children);

  const onScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    const firstItem = el.querySelector<HTMLElement>("[data-slider-item]");
    if (!firstItem) return;
    const gapPx = 12;
    const itemWidth = firstItem.offsetWidth + gapPx;
    const idx = Math.round(el.scrollLeft / itemWidth);
    setActive(Math.max(0, Math.min(count - 1, idx)));
  };

  return (
    <div className="mb-5">
      <div
        ref={scrollRef}
        onScroll={onScroll}
        className="overflow-x-auto"
        style={{
          scrollSnapType: "x mandatory",
          scrollbarWidth: "none",
          WebkitOverflowScrolling: "touch",
        }}
      >
        <div className="flex items-stretch gap-3 px-5 pb-1">{children}</div>
      </div>
      {count > 1 ? (
        <div className="mt-3 flex justify-center gap-1.5">
          {Array.from({ length: count }).map((_, i) => (
            <span
              key={i}
              className="h-1.5 rounded-full transition-all duration-200"
              style={{
                width: i === active ? 18 : 6,
                background: i === active ? GRAD_METALLIC_SUBTLE : C.border,
              }}
            />
          ))}
        </div>
      ) : null}
    </div>
  );
}

type ItemProps = { children: ReactNode };

export function AnalyticsSliderItem({ children }: ItemProps) {
  return (
    <div
      data-slider-item
      className="flex-shrink-0"
      style={{
        width: "85vw",
        maxWidth: 360,
        minWidth: 280,
        scrollSnapAlign: "start",
      }}
    >
      {children}
    </div>
  );
}
