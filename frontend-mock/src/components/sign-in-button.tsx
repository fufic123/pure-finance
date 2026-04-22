"use client";

import type { ButtonHTMLAttributes } from "react";
import { motion } from "framer-motion";
import { GOLD_TEXT_STYLE } from "@/lib/tokens";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { dark?: boolean };

/**
 * Landing "Continue with Google" CTA — black pill with gold-text label
 * (background-clip: text). Matches LandingB reference.
 */
export function SignInButton({ children, className = "", dark = false, ...rest }: Props) {
  return (
    <motion.button
      type="button"
      whileTap={{ scale: 0.97 }}
      {...rest}
      className={
        "relative flex h-[52px] w-full items-center justify-center rounded-[14px] " +
        "text-[16px] font-semibold select-none transition " +
        "active:opacity-90 disabled:pointer-events-none disabled:opacity-50 " +
        className
      }
      style={{ background: dark ? "#FFFFFF" : "#0A0A0A" }}
    >
      <span style={GOLD_TEXT_STYLE}>{children}</span>
    </motion.button>
  );
}
