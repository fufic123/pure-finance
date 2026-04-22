import { GRAD_METALLIC, pfTheme } from "@/lib/tokens";

type Props = { dark?: boolean };

/**
 * Small Pure Finance wordmark used at the top of LandingB — gold dot + label.
 */
export function BrandMark({ dark = false }: Props) {
  const C = pfTheme(dark);
  return (
    <div className="flex items-center gap-1.5">
      <div className="h-2 w-2 rounded-full" style={{ background: GRAD_METALLIC }} />
      <span
        className="text-[14px] font-medium tracking-[0.2px]"
        style={{ color: C.text }}
      >
        Pure Finance
      </span>
    </div>
  );
}
