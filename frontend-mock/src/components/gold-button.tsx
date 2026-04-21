"use client";

import type { ButtonHTMLAttributes } from "react";
import { motion } from "framer-motion";

type Props = ButtonHTMLAttributes<HTMLButtonElement>;

export function GoldButton({ children, className = "", ...rest }: Props) {
  return (
    <motion.button
      type="button"
      whileTap={{ scale: 0.97 }}
      {...rest}
      className={
        "relative h-[52px] w-full rounded-[14px] bg-gold-metallic text-pf-black " +
        "text-base font-semibold select-none transition " +
        "active:opacity-90 disabled:pointer-events-none disabled:opacity-50 " +
        className
      }
    >
      {children}
    </motion.button>
  );
}
