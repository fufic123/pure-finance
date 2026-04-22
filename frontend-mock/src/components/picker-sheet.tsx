"use client";

import { AnimatePresence, motion } from "framer-motion";
import { PF, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

export type PickerItem = {
  id: string;
  label: string;
  sublabel?: string;
};

type Props = {
  open: boolean;
  title: string;
  items: PickerItem[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onClose: () => void;
};

export function PickerSheet({
  open,
  title,
  items,
  selectedId,
  onSelect,
  onClose,
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
            initial={{ y: 400 }}
            animate={{ y: 0 }}
            exit={{ y: 400 }}
            transition={{ duration: 0.22, ease: "easeOut" }}
            onClick={(e) => e.stopPropagation()}
            className="max-h-[75vh] w-full overflow-y-auto rounded-t-[20px] p-5"
            style={{ background: surface, border: `1px solid ${C.border}` }}
          >
            <div
              className="mx-auto mb-4 h-1 w-10 rounded-full"
              style={{ background: C.border }}
            />
            <h3
              className="mb-3 text-[17px] font-semibold"
              style={{ color: C.text }}
            >
              {title}
            </h3>
            <div className="flex flex-col gap-1.5">
              {items.map((it) => {
                const on = it.id === selectedId;
                return (
                  <button
                    key={it.id}
                    type="button"
                    onClick={() => {
                      onSelect(it.id);
                      onClose();
                    }}
                    className="flex h-[52px] w-full items-center justify-between rounded-[12px] px-4 text-left"
                    style={{
                      border: `1px solid ${C.border}`,
                      background: on
                        ? dark
                          ? "rgba(201,162,39,0.08)"
                          : "rgba(201,162,39,0.06)"
                        : "transparent",
                    }}
                  >
                    <div>
                      <div
                        className="text-[15px]"
                        style={{ color: C.text }}
                      >
                        {it.label}
                      </div>
                      {it.sublabel ? (
                        <div
                          className="mt-[1px] text-[12px]"
                          style={{ color: C.muted }}
                        >
                          {it.sublabel}
                        </div>
                      ) : null}
                    </div>
                    {on ? (
                      <span style={{ color: PF.goldBase, fontSize: 16 }}>✓</span>
                    ) : null}
                  </button>
                );
              })}
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
