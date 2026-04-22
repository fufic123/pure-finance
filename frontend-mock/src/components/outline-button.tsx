"use client";

import type { ButtonHTMLAttributes } from "react";
import { motion } from "framer-motion";
import { pfTheme } from "@/lib/tokens";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { dark?: boolean };

export function OutlineButton({ children, className = "", dark = false, ...rest }: Props) {
  const C = pfTheme(dark);
  return (
    <motion.button
      type="button"
      whileTap={{ scale: 0.97 }}
      {...rest}
      className={
        "flex h-12 w-full items-center justify-center gap-2 rounded-[12px] " +
        "text-[15px] font-medium select-none " +
        "disabled:pointer-events-none disabled:opacity-50 " +
        className
      }
      style={{
        border: `1.5px solid ${C.border}`,
        color: C.text,
        background: "transparent",
      }}
    >
      {children}
    </motion.button>
  );
}
