"use client";

import { AnimatePresence, motion } from "framer-motion";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

export type ActionItem = {
  label: string;
  destructive?: boolean;
  onClick: () => void;
};

type Props = {
  open: boolean;
  onClose: () => void;
  actions: ActionItem[];
};

export function ActionSheet({ open, onClose, actions }: Props) {
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const surface = dark ? "#1A1A1A" : "#FFFFFF";

  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="pf-safe-bottom fixed inset-0 z-[60] flex items-end bg-black/50"
          onClick={onClose}
        >
          <motion.div
            initial={{ y: 300 }}
            animate={{ y: 0 }}
            exit={{ y: 300 }}
            transition={{ duration: 0.22, ease: "easeOut" }}
            onClick={(e) => e.stopPropagation()}
            className="w-full px-3 pb-3"
          >
            <div
              className="mb-2 overflow-hidden rounded-[14px]"
              style={{ background: surface, border: `1px solid ${C.border}` }}
            >
              {actions.map((a, i) => (
                <button
                  key={a.label}
                  type="button"
                  onClick={() => {
                    a.onClick();
                    onClose();
                  }}
                  className="flex h-[52px] w-full items-center justify-center text-[16px]"
                  style={{
                    color: a.destructive ? "#B03A2E" : C.text,
                    fontWeight: a.destructive ? 500 : 400,
                    borderTop: i > 0 ? `1px solid ${C.subtleBorder}` : "none",
                  }}
                >
                  {a.label}
                </button>
              ))}
            </div>
            <button
              type="button"
              onClick={onClose}
              className="flex h-[52px] w-full items-center justify-center rounded-[14px] text-[16px] font-semibold"
              style={{
                background: surface,
                border: `1px solid ${C.border}`,
                color: C.text,
              }}
            >
              Cancel
            </button>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
