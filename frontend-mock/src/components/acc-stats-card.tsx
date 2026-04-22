import { GRAD_METALLIC_SUBTLE, PF, pfTheme } from "@/lib/tokens";
import { MOCK_CATEGORIES, MOCK_SUMMARY } from "@/lib/mock";

type Props = { dark?: boolean };

export function AccStatsCard({ dark = false }: Props) {
  const C = pfTheme(dark);
  const dots = ["#0A0A0A", "#4A4A4A", "#8A8A8A", "#BBBBBB"];
  const cats = MOCK_CATEGORIES.slice(0, 4);

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
        April 2026
      </div>
      <div className="mb-3.5 flex justify-between">
        <Stat
          label="Spent"
          value={`−€${MOCK_SUMMARY.expenses}`}
          color={PF.expense}
          align="left"
          dark={dark}
        />
        <Stat
          label="Transactions"
          value={`${MOCK_SUMMARY.count}`}
          color={C.text}
          align="center"
          dark={dark}
        />
        <Stat label="Avg / day" value="€51" color={C.text} align="right" dark={dark} />
      </div>
      <div style={{ borderTop: `1px solid ${C.border}` }}>
        {cats.map((cat, i) => (
          <div
            key={cat.name}
            className="flex items-center justify-between py-[7px]"
            style={{
              borderBottom: i < cats.length - 1 ? `1px solid ${C.subtleBorder}` : "none",
            }}
          >
            <div className="flex items-center gap-2">
              <span
                className="inline-block h-[7px] w-[7px] rounded-full"
                style={{ background: dots[i] ?? "#555" }}
              />
              <span className="text-[13px]" style={{ color: C.text }}>
                {cat.name}
              </span>
            </div>
            <div className="flex items-center gap-2.5">
              <div
                className="h-[2px] w-12 overflow-hidden rounded-[1px]"
                style={{ background: C.border }}
              >
                <div
                  className="h-full rounded-[1px]"
                  style={{ width: `${cat.pct}%`, background: GRAD_METALLIC_SUBTLE }}
                />
              </div>
              <span
                className="w-14 text-right text-[13px] tabular-nums"
                style={{ color: C.muted }}
              >
                −€{cat.total}
              </span>
            </div>
          </div>
        ))}
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
  const alignClass =
    align === "left" ? "text-left" : align === "right" ? "text-right" : "text-center";
  return (
    <div className={alignClass}>
      <div className="mb-[3px] text-[11px]" style={{ color: C.muted }}>
        {label}
      </div>
      <div className="text-[15px] font-semibold tabular-nums" style={{ color }}>
        {value}
      </div>
    </div>
  );
}
