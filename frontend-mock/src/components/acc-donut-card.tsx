import { GOLD_TEXT_STYLE, pfTheme } from "@/lib/tokens";

type Props = { dark?: boolean };

type Cat = { name: string; pct: number; color: string };

const CATS: Cat[] = [
  { name: "Food", pct: 31, color: "#0A0A0A" },
  { name: "Groceries", pct: 21, color: "#4A4A4A" },
  { name: "Transport", pct: 12, color: "#8A8A8A" },
  { name: "Entertainment", pct: 10, color: "#BBBBBB" },
  { name: "Other", pct: 26, color: "#DEDEDE" },
];

export function AccDonutCard({ dark = false }: Props) {
  const C = pfTheme(dark);
  const r = 40;
  const size = 120;
  const cx = size / 2;
  const cy = size / 2;
  const circ = 2 * Math.PI * r;

  let acc = 0;
  const segs = CATS.map((cat) => {
    const dash = (cat.pct / 100) * circ;
    const offset = -acc;
    acc += dash;
    return { ...cat, dash, offset };
  });

  return (
    <div
      className="mx-5 mb-5 rounded-[13px] p-4"
      style={{
        background: dark ? "#1A1A1A" : "#F7F7F7",
        border: `1px solid ${C.border}`,
      }}
    >
      <div
        className="mb-4 text-[12px] font-semibold uppercase tracking-[0.4px]"
        style={{ color: C.muted }}
      >
        Spending breakdown · April
      </div>
      <div className="flex items-center gap-4">
        <div className="relative flex-shrink-0" style={{ width: size, height: size }}>
          <svg
            width={size}
            height={size}
            style={{ transform: "rotate(-90deg)", display: "block" }}
          >
            <circle
              cx={cx}
              cy={cy}
              r={r}
              fill="none"
              stroke={dark ? "#2A2A2A" : "#EEEEEE"}
              strokeWidth={16}
            />
            {segs.map((seg) => (
              <circle
                key={seg.name}
                cx={cx}
                cy={cy}
                r={r}
                fill="none"
                stroke={seg.color}
                strokeWidth={16}
                strokeDasharray={`${seg.dash} ${circ}`}
                strokeDashoffset={seg.offset}
              />
            ))}
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div
              className="text-[14px] font-bold leading-none tabular-nums"
              style={GOLD_TEXT_STYLE}
            >
              −€1,540
            </div>
            <div className="mt-0.5 text-[10px]" style={{ color: C.muted }}>
              total
            </div>
          </div>
        </div>
        <div className="flex flex-1 flex-col gap-[7px]">
          {CATS.map((cat) => (
            <div key={cat.name} className="flex items-center justify-between">
              <div className="flex items-center gap-[7px]">
                <div
                  className="h-2 w-2 flex-shrink-0 rounded-[2px]"
                  style={{ background: cat.color }}
                />
                <span className="text-[12px]" style={{ color: C.text }}>
                  {cat.name}
                </span>
              </div>
              <span className="text-[12px] tabular-nums" style={{ color: C.muted }}>
                {cat.pct}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
