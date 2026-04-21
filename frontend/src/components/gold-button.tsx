"use client";

import type { ButtonHTMLAttributes } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement>;

export function GoldButton({ children, className = "", ...rest }: Props) {
  return (
    <button
      type="button"
      {...rest}
      className={
        "relative h-[52px] w-full rounded-[14px] bg-gold-metallic text-pf-black " +
        "text-base font-semibold select-none transition " +
        "active:opacity-90 disabled:pointer-events-none disabled:opacity-50 " +
        className
      }
    >
      {children}
    </button>
  );
}
