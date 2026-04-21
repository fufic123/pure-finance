import { GRAD_METALLIC_SUBTLE } from "@/lib/tokens";

type Props = {
  name: string;
  count: number;
  total: string;
  pct: number;
  dotColor: string;
  muted?: boolean;
};

export function CategoryBar({ name, count, total, pct, dotColor, muted = false }: Props) {
  return (
    <div
      className={"flex flex-col gap-2 border-b border-white/[0.06] px-5 py-3 " + (muted ? "opacity-60" : "")}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span
            className="inline-block h-2 w-2 flex-shrink-0 rounded-full"
            style={{ background: dotColor }}
          />
          <div>
            <div className="text-[15px] text-pf-white">{name}</div>
            <div className="text-[11px] text-white/40">
              {count} {count === 1 ? "transaction" : "transactions"} · {pct}% of spend
            </div>
          </div>
        </div>
        <div className="text-[15px] font-medium tabular-nums text-pf-white">−€{total}</div>
      </div>
      <div className="h-[2px] w-full rounded-[1px] bg-white/[0.08]">
        <div
          className="h-full rounded-[1px]"
          style={{ width: `${pct}%`, background: GRAD_METALLIC_SUBTLE }}
        />
      </div>
    </div>
  );
}
