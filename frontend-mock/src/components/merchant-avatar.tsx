type Props = {
  glyph?: string;
  background?: string;
  size?: number;
};

/**
 * Merchant avatar chip — rounded square with an emoji/glyph centered.
 * Used on the Transaction Detail hero.
 */
export function MerchantAvatar({
  glyph = "\u{1F6F5}",
  background = "#191C1F",
  size = 52,
}: Props) {
  return (
    <div
      className="mx-auto flex items-center justify-center rounded-[14px]"
      style={{
        width: size,
        height: size,
        background,
        fontSize: Math.round(size * 0.42),
      }}
    >
      <span aria-hidden>{glyph}</span>
    </div>
  );
}
