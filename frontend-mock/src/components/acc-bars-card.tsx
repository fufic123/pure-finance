import { PF, pfTheme } from "@/lib/tokens";
import { MOCK_SPEND_TREND } from "@/lib/mock";

type Props = { dark?: boolean };

export function AccBarsCard({ dark = false }: Props) {
  const C = pfTheme(dark);
  const data = MOCK_SPEND_TREND;

  const tw = 280;
  const th = 72;
  const padX = 8;
  const padY = 8;
  const maxV = Math.max(...data.map((d) => d.v));
  const minV = Math.min(...data.map((d) => d.v));
  const range = maxV - minV || 1;

  const pts = data.map((d, i) => ({
    x: padX + (i / (data.length - 1)) * (tw - padX * 2),
    y: padY + (1 - (d.v - minV) / range) * (th - padY * 2),
  }));

  const smoothPath = pts.reduce((acc, p, i) => {
    if (i === 0) return `M${p.x},${p.y}`;
    const prev = pts[i - 1]!;
    const cp1x = prev.x + (p.x - prev.x) * 0.45;
    const cp2x = p.x - (p.x - prev.x) * 0.45;
    return `${acc} C${cp1x},${prev.y} ${cp2x},${p.y} ${p.x},${p.y}`;
  }, "");

  const last = pts[pts.length - 1]!;
  const first = pts[0]!;
  const areaPath = `${smoothPath} L${last.x},${th + padY} L${first.x},${th + padY} Z`;

  return (
    <div
      className="mx-5 mb-5 rounded-[13px] p-4"
      style={{
        background: dark ? "#1A1A1A" : "#F7F7F7",
        border: `1px solid ${C.border}`,
      }}
    >
      <div
        className="mb-3.5 text-[12px] font-semibold uppercase tracking-[0.4px]"
        style={{ color: C.muted }}
      >
        Monthly spending
      </div>

      <div className="mb-4 flex justify-between">
        <Stat label="This month" value="−€1,540" color={PF.expense} align="left" dark={dark} />
        <Stat label="Last month" value="−€1,320" color={C.muted} align="center" dark={dark} />
        <Stat label="Δ vs prior" value="+16%" color={PF.expense} align="right" dark={dark} />
      </div>

      <svg
        width="100%"
        height={th + padY * 2}
        viewBox={`0 0 ${tw} ${th + padY * 2}`}
        style={{ display: "block", overflow: "visible" }}
        preserveAspectRatio="none"
      >
        <defs>
          <linearGradient id="barsAreaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={PF.goldBase} stopOpacity={dark ? "0.22" : "0.18"} />
            <stop offset="100%" stopColor={PF.goldBase} stopOpacity="0.01" />
          </linearGradient>
        </defs>
        <path d={areaPath} fill="url(#barsAreaGrad)" />
        <path
          d={smoothPath}
          fill="none"
          stroke={PF.goldBase}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {pts.map((p, i) => (
          <circle
            key={i}
            cx={p.x}
            cy={p.y}
            r="2.5"
            fill={i === pts.length - 1 ? PF.goldBase : dark ? "#3A3A3A" : "#D0D0D0"}
            stroke={i === pts.length - 1 ? PF.goldBase : dark ? "#2A2A2A" : "#F7F7F7"}
            strokeWidth="1.5"
          />
        ))}
        <circle cx={last.x} cy={last.y} r="5" fill={PF.goldBase} />
        <circle
          cx={last.x}
          cy={last.y}
          r="8.5"
          fill="none"
          stroke={PF.goldBase}
          strokeWidth="1"
          strokeOpacity="0.35"
        />
      </svg>

      <div className="mt-1 flex justify-between">
        {data.map((d, i) => {
          const isLast = i === data.length - 1;
          return (
            <span
              key={d.m}
              className="text-[10px]"
              style={{
                color: isLast ? PF.goldBase : C.muted,
                fontWeight: isLast ? 600 : 400,
              }}
            >
              {d.m}
            </span>
          );
        })}
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  color,
  align,
  dark,
}: {
  label: string;
  value: string;
  color: string;
  align: "left" | "center" | "right";
  dark: boolean;
}) {
  const C = pfTheme(dark);
  const cls =
    align === "left" ? "text-left" : align === "right" ? "text-right" : "text-center";
  return (
    <div className={cls}>
      <div className="mb-[3px] text-[11px]" style={{ color: C.muted }}>
        {label}
      </div>
      <div className="text-[14px] font-semibold tabular-nums" style={{ color }}>
        {value}
      </div>
    </div>
  );
}
