import { GOLD_TEXT_STYLE, PF } from "@/lib/tokens";
import type { MockSummary } from "@/lib/mock";

type Props = { summary: MockSummary };

export function SummaryCard({ summary }: Props) {
  return (
    <div className="flex border-b border-white/[0.06] px-5 pb-3.5 pt-2.5">
      <Col label="Income" value={`+€${summary.income}`} color={PF.income} />
      <Divider />
      <Col label="Spend" value={`−€${summary.expenses}`} color={PF.expense} />
      <Divider />
      <GoldCol label="Net" value={`+€${summary.net}`} />
    </div>
  );
}

function Col({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className="min-w-0 flex-1">
      <div className="mb-[3px] text-[11px] uppercase tracking-[0.3px] text-white/40">{label}</div>
      <div
        className="text-[13px] font-semibold tabular-nums"
        style={{ color }}
      >
        {value}
      </div>
    </div>
  );
}

function GoldCol({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 flex-1">
      <div className="mb-[3px] text-[11px] uppercase tracking-[0.3px] text-white/40">{label}</div>
      <div className="text-[13px] font-bold tabular-nums" style={GOLD_TEXT_STYLE}>
        {value}
      </div>
    </div>
  );
}

function Divider() {
  return <div className="mx-3.5 w-px self-stretch bg-white/[0.08]" />;
}
