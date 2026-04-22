import { GRAD_METALLIC_SUBTLE, pfTheme } from "@/lib/tokens";

type Props = {
  name: string;
  count: number;
  total: string;
  pct: number;
  dotColor: string;
  muted?: boolean;
  dark?: boolean;
};

export function CategoryBar({
  name,
  count,
  total,
  pct,
  dotColor,
  muted = false,
  dark = false,
}: Props) {
  const C = pfTheme(dark);
  return (
    <div
      className={"flex flex-col gap-2 px-5 py-3 " + (muted ? "opacity-60" : "")}
      style={{ borderBottom: `1px solid ${C.subtleBorder}` }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span
            className="inline-block h-2 w-2 flex-shrink-0 rounded-full"
            style={{ background: dotColor }}
          />
          <div>
            <div className="text-[15px]" style={{ color: C.text }}>
              {name}
            </div>
            <div className="text-[11px]" style={{ color: C.muted }}>
              {count} {count === 1 ? "transaction" : "transactions"} · {pct}% of spend
            </div>
          </div>
        </div>
        <div
          className="text-[15px] font-medium tabular-nums"
          style={{ color: C.text }}
        >
          −€{total}
        </div>
      </div>
      <div
        className="h-[2px] w-full rounded-[1px]"
        style={{ background: C.border }}
      >
        <div
          className="h-full rounded-[1px]"
          style={{ width: `${pct}%`, background: GRAD_METALLIC_SUBTLE }}
        />
      </div>
    </div>
  );
}
