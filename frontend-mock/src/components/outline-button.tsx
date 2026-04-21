"use client";

import type { ButtonHTMLAttributes } from "react";
import { motion } from "framer-motion";

type Props = ButtonHTMLAttributes<HTMLButtonElement>;

export function OutlineButton({ children, className = "", ...rest }: Props) {
  return (
    <motion.button
      type="button"
      whileTap={{ scale: 0.97 }}
      {...rest}
      className={
        "flex h-12 w-full items-center justify-center gap-2 rounded-[12px] " +
        "border border-white/15 text-pf-white text-[15px] font-medium select-none " +
        "active:bg-white/5 disabled:pointer-events-none disabled:opacity-50 " +
        className
      }
    >
      {children}
    </motion.button>
  );
}
