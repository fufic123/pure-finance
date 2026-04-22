import { GRAD_METALLIC, GRAD_METALLIC_SUBTLE, PF, pfTheme } from "@/lib/tokens";
import { MOCK_AI_INSIGHTS, MOCK_SPEND_TREND } from "@/lib/mock";

type Props = { dark?: boolean; embedded?: boolean };

export function AccAICard({ dark = false, embedded = false }: Props) {
  const C = pfTheme(dark);
  const data = MOCK_SPEND_TREND;

  const tw = 280;
  const th = 60;
  const padX = 6;
  const padY = 6;
  const maxV = Math.max(...data.map((d) => d.v));
  const minV = Math.min(...data.map((d) => d.v));
  const range = maxV - minV || 1;

  const pts = data.map((d, i) => ({
    x: padX + (i / (data.length - 1)) * (tw - padX * 2),
    y: padY + (1 - (d.v - minV) / range) * (th - padY * 2),
  }));

  const line = pts.reduce((acc, p, i) => {
    if (i === 0) return `M${p.x},${p.y}`;
    const prev = pts[i - 1]!;
    const cp1x = prev.x + (p.x - prev.x) * 0.45;
    const cp2x = p.x - (p.x - prev.x) * 0.45;
    return `${acc} C${cp1x},${prev.y} ${cp2x},${p.y} ${p.x},${p.y}`;
  }, "");

  const last = pts[pts.length - 1]!;
  const prev = pts[pts.length - 2]!;
  const first = pts[0]!;
  const area = `${line} L${last.x},${th + padY} L${first.x},${th + padY} Z`;
  const colW = (tw - padX * 2) / (data.length - 1);

  const segLastTwo = `M${prev.x},${prev.y} C${prev.x + (last.x - prev.x) * 0.45},${prev.y} ${last.x - (last.x - prev.x) * 0.45},${last.y} ${last.x},${last.y}`;

  return (
    <div
      className={
        (embedded ? "h-full " : "mx-5 mb-5 ") + "rounded-[13px] p-4"
      }
      style={{
        background: dark ? "#1A1A1A" : "#F7F7F7",
        border: `1px solid ${C.border}`,
      }}
    >
      {/* Header */}
      <div className="mb-3.5 flex items-center gap-2">
        <div
          className="flex h-[22px] w-[22px] flex-shrink-0 items-center justify-center rounded-[6px]"
          style={{ background: GRAD_METALLIC }}
        >
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M6 1l1.2 3.8L11 6 7.2 7.2 6 11 4.8 7.2 1 6l3.8-1.2z" fill="#0A0A0A" />
          </svg>
        </div>
        <span className="text-[13px] font-semibold" style={{ color: C.text }}>
          Insights
        </span>
        <span className="text-[11px]" style={{ color: C.muted }}>
          · AI summary
        </span>
      </div>

      {/* Trend graph */}
      <div className="mb-3.5">
        <div className="mb-1.5 flex items-baseline justify-between">
          <span className="text-[11px]" style={{ color: C.muted }}>
            Spend trend · 6 months
          </span>
          <span
            className="text-[11px] font-semibold tabular-nums"
            style={{ color: PF.expense }}
          >
            Apr +16% vs Mar
          </span>
        </div>
        <svg
          width="100%"
          height={th + padY * 2}
          viewBox={`0 0 ${tw} ${th + padY * 2}`}
          style={{ display: "block", overflow: "visible" }}
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="aiGrad2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={PF.goldBase} stopOpacity={dark ? "0.2" : "0.15"} />
              <stop offset="100%" stopColor={PF.goldBase} stopOpacity="0.01" />
            </linearGradient>
          </defs>
          {/* Current-month column highlight */}
          <rect
            x={last.x - colW / 2}
            y={padY}
            width={colW}
            height={th}
            fill={PF.goldBase}
            fillOpacity={dark ? "0.07" : "0.06"}
            rx="3"
          />
          <text
            x={last.x}
            y={padY - 2}
            textAnchor="middle"
            fontSize="8.5"
            fill={PF.goldBase}
            fontFamily="Inter,sans-serif"
            fontWeight="600"
          >
            This month
          </text>
          <path d={area} fill="url(#aiGrad2)" />
          <path
            d={line}
            fill="none"
            stroke={dark ? "#4A4A4A" : "#D0D0D0"}
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d={segLastTwo}
            fill="none"
            stroke={PF.goldBase}
            strokeWidth="2"
            strokeLinecap="round"
          />
          <circle
            cx={prev.x}
            cy={prev.y}
            r="3"
            fill={dark ? "#3A3A3A" : "#C8C8C8"}
            stroke={dark ? "#2A2A2A" : "#F7F7F7"}
            strokeWidth="1.5"
          />
          <circle cx={last.x} cy={last.y} r="4.5" fill={PF.goldBase} />
          <circle
            cx={last.x}
            cy={last.y}
            r="7.5"
            fill="none"
            stroke={PF.goldBase}
            strokeWidth="1"
            strokeOpacity="0.3"
          />
        </svg>
        <div className="mt-[3px] flex justify-between">
          {data.map((d, i) => {
            const isLast = i === data.length - 1;
            return (
              <span
                key={d.m}
                style={{
                  fontSize: "9.5px",
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

      <div style={{ height: 1, background: C.border, marginBottom: 12 }} />

      <div className="flex flex-col gap-[9px]">
        {MOCK_AI_INSIGHTS.map((item, i) => (
          <div key={i} className="flex items-start gap-2.5">
            <div
              className="flex-shrink-0"
              style={{
                width: 2.5,
                minHeight: 34,
                borderRadius: 2,
                background: GRAD_METALLIC_SUBTLE,
                marginTop: 2,
              }}
            />
            <p
              className="m-0"
              style={{ fontSize: 12.5, color: C.text, lineHeight: 1.45 }}
            >
              {item.text}
            </p>
          </div>
        ))}
      </div>

      {/* Savings tip */}
      <div
        className="mt-3.5 flex items-start gap-2.5 rounded-[10px] px-3.5 py-2.5"
        style={{
          background: dark ? "rgba(201,162,39,0.08)" : "rgba(201,162,39,0.07)",
          border: "1px solid rgba(201,162,39,0.2)",
        }}
      >
        <div
          className="flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-[5px]"
          style={{ background: GRAD_METALLIC, marginTop: 1 }}
        >
          <svg
            width="10"
            height="10"
            viewBox="0 0 10 10"
            fill="none"
            stroke="#0A0A0A"
            strokeWidth="1.4"
            strokeLinecap="round"
          >
            <path d="M5 1v4M5 8v.5M2 3.5C2 2 3.3 1 5 1c1.7 0 3 1 3 2.5 0 2-2 2.5-3 4" />
          </svg>
        </div>
        <p
          className="m-0"
          style={{ fontSize: 12.5, color: C.text, lineHeight: 1.45 }}
        >
          <span style={{ fontWeight: 600 }}>Save tip: </span>
          Setting a €600 budget for Food &amp; Groceries could save you ~€200/month based on your last 3 months.
        </p>
      </div>
    </div>
  );
}
