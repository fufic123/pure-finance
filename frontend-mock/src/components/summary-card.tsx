import { GOLD_TEXT_STYLE, PF, pfTheme } from "@/lib/tokens";
import type { MockSummary } from "@/lib/mock";

type Props = { summary: MockSummary; dark?: boolean };

export function SummaryCard({ summary, dark = false }: Props) {
  const C = pfTheme(dark);
  return (
    <div
      className="flex px-5 pb-3.5 pt-2.5"
      style={{ borderBottom: `1px solid ${C.border}` }}
    >
      <Col label="Income" value={`+€${summary.income}`} color={PF.income} dark={dark} />
      <Divider dark={dark} />
      <Col label="Spend" value={`−€${summary.expenses}`} color={PF.expense} dark={dark} />
      <Divider dark={dark} />
      <GoldCol label="Net" value={`+€${summary.net}`} dark={dark} />
    </div>
  );
}

function Col({
  label,
  value,
  color,
  dark,
}: {
  label: string;
  value: string;
  color: string;
  dark: boolean;
}) {
  const C = pfTheme(dark);
  return (
    <div className="min-w-0 flex-1">
      <div
        className="mb-[3px] text-[11px] uppercase tracking-[0.3px]"
        style={{ color: C.muted }}
      >
        {label}
      </div>
      <div className="text-[13px] font-semibold tabular-nums" style={{ color }}>
        {value}
      </div>
    </div>
  );
}

function GoldCol({ label, value, dark }: { label: string; value: string; dark: boolean }) {
  const C = pfTheme(dark);
  return (
    <div className="min-w-0 flex-1">
      <div
        className="mb-[3px] text-[11px] uppercase tracking-[0.3px]"
        style={{ color: C.muted }}
      >
        {label}
      </div>
      <div className="text-[13px] font-bold tabular-nums" style={GOLD_TEXT_STYLE}>
        {value}
      </div>
    </div>
  );
}

function Divider({ dark }: { dark: boolean }) {
  const C = pfTheme(dark);
  return <div className="mx-3.5 w-px self-stretch" style={{ background: C.border }} />;
}
