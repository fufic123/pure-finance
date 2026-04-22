import type { ReactNode } from "react";

type Props = { children: ReactNode };

export function AnalyticsSlider({ children }: Props) {
  return (
    <div
      className="mb-5 overflow-x-auto"
      style={{
        scrollSnapType: "x mandatory",
        scrollbarWidth: "none",
        WebkitOverflowScrolling: "touch",
      }}
    >
      <div className="flex gap-3 px-5 pb-1">{children}</div>
    </div>
  );
}

type ItemProps = { children: ReactNode };

export function AnalyticsSliderItem({ children }: ItemProps) {
  return (
    <div
      className="flex-shrink-0"
      style={{ width: "85vw", maxWidth: 360, minWidth: 280, scrollSnapAlign: "start" }}
    >
      {children}
    </div>
  );
}
