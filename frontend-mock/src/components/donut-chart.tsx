import { GOLD_TEXT_STYLE } from "@/lib/tokens";

type Segment = {
  label: string;
  pct: number;
  color: string;
};

type Props = {
  size?: number;
  thickness?: number;
  segments: Segment[];
  centerLabel: string;
  centerSub?: string;
  focusedIndex?: number;
};

export function DonutChart({
  size = 140,
  thickness = 18,
  segments,
  centerLabel,
  centerSub = "total",
  focusedIndex,
}: Props) {
  const r = (size - thickness) / 2;
  const cx = size / 2;
  const cy = size / 2;
  const circ = 2 * Math.PI * r;
  let acc = 0;

  // If a segment is focused, paint it with gold subtle gradient via a url ref.
  const gradId = "pf-donut-gold-subtle";

  return (
    <div className="relative flex-shrink-0" style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        style={{ transform: "rotate(-90deg)", display: "block" }}
      >
        <defs>
          <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#C9A227" />
            <stop offset="50%" stopColor="#E8D178" />
            <stop offset="100%" stopColor="#C9A227" />
          </linearGradient>
        </defs>
        {/* Track */}
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth={thickness}
        />
        {segments.map((seg, i) => {
          const dash = (seg.pct / 100) * circ;
          const offset = -acc;
          acc += dash;
          const isFocus = focusedIndex === i;
          return (
            <circle
              key={seg.label}
              cx={cx}
              cy={cy}
              r={r}
              fill="none"
              stroke={isFocus ? `url(#${gradId})` : seg.color}
              strokeWidth={thickness}
              strokeDasharray={`${dash} ${circ}`}
              strokeDashoffset={offset}
            />
          );
        })}
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <div
          className="text-[16px] font-bold leading-none tabular-nums"
          style={GOLD_TEXT_STYLE}
        >
          {centerLabel}
        </div>
        <div className="mt-1 text-[10px] text-white/40">{centerSub}</div>
      </div>
    </div>
  );
}
