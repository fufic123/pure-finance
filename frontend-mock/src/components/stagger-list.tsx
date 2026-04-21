"use client";

import { motion, type Variants } from "framer-motion";
import type { HTMLAttributes, ReactNode } from "react";

const container: Variants = {
  hidden: { opacity: 1 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.03 },
  },
};

export const staggerItem: Variants = {
  hidden: { opacity: 0, y: 6 },
  show: { opacity: 1, y: 0, transition: { duration: 0.15, ease: "easeOut" } },
};

type Props = HTMLAttributes<HTMLUListElement> & { children: ReactNode };

export function StaggerList({ children, className = "", ...rest }: Props) {
  return (
    <motion.ul
      variants={container}
      initial="hidden"
      animate="show"
      className={className}
      {...rest}
    >
      {children}
    </motion.ul>
  );
}

export function StaggerItem({
  children,
  className = "",
  ...rest
}: HTMLAttributes<HTMLLIElement> & { children: ReactNode }) {
  return (
    <motion.li variants={staggerItem} className={className} {...rest}>
      {children}
    </motion.li>
  );
}
