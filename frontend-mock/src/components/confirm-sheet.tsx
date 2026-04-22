"use client";

import { AnimatePresence, motion } from "framer-motion";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

type Props = {
  open: boolean;
  title: string;
  body?: string;
  confirmLabel: string;
  destructive?: boolean;
  onClose: () => void;
  onConfirm: () => void;
};

export function ConfirmSheet({
  open,
  title,
  body,
  confirmLabel,
  destructive = false,
  onClose,
  onConfirm,
}: Props) {
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
            className="w-full rounded-t-[20px] p-5"
            style={{ background: surface, border: `1px solid ${C.border}` }}
          >
            <div
              className="mx-auto mb-4 h-1 w-10 rounded-full"
              style={{ background: C.border }}
            />
            <h3
              className="mb-2 text-[17px] font-semibold"
              style={{ color: C.text }}
            >
              {title}
            </h3>
            {body ? (
              <p
                className="mb-5 text-[14px] leading-[1.45]"
                style={{ color: C.muted }}
              >
                {body}
              </p>
            ) : null}
            <div className="flex gap-3">
              <button
                type="button"
                onClick={onClose}
                className="flex h-12 flex-1 items-center justify-center rounded-[12px] text-[15px]"
                style={{ border: `1px solid ${C.border}`, color: C.text }}
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => {
                  onConfirm();
                  onClose();
                }}
                className="flex h-12 flex-1 items-center justify-center rounded-[12px] text-[15px] font-semibold"
                style={
                  destructive
                    ? { background: "#B03A2E", color: "#FFFFFF" }
                    : { background: C.text, color: C.bg }
                }
              >
                {confirmLabel}
              </button>
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
