"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { MOCK_CATEGORY_TREE, MOCK_TRANSACTIONS } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { TopBar } from "@/components/top-bar";
import { GoldButton } from "@/components/gold-button";
import { FormRow } from "@/components/form-row";
import { PickerSheet, type PickerItem } from "@/components/picker-sheet";

function flattenCategories(): PickerItem[] {
  const items: PickerItem[] = [{ id: "", label: "Uncategorized" }];
  for (const parent of MOCK_CATEGORY_TREE) {
    items.push({ id: parent.id, label: parent.name });
    for (const child of parent.children) {
      items.push({
        id: child.id,
        label: child.name,
        sublabel: parent.name,
      });
    }
  }
  return items;
}

export default function EditTransactionPage() {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const tx = MOCK_TRANSACTIONS[0]!;

  const categories = useMemo(flattenCategories, []);
  const [description, setDescription] = useState(tx.desc);
  const [date, setDate] = useState("2026-04-21");
  const [categoryId, setCategoryId] = useState<string | null>("cat-food");
  const [note, setNote] = useState("");
  const [categoryPickerOpen, setCategoryPickerOpen] = useState(false);

  const cat = categories.find((c) => c.id === categoryId);

  return (
    <PageTransition>
      <main className="min-h-screen pb-10" style={{ background: C.bg }}>
        <TopBar title="Edit transaction" back />

        <div className="mx-4 mt-3 overflow-hidden rounded-[14px]" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
          <FormRow label="Account">
            <span style={{ color: C.muted }}>Revolut</span>
          </FormRow>
          <FormRow label="Amount">
            <span style={{ color: C.muted }} className="tabular-nums">
              {tx.amount}
            </span>
          </FormRow>
          <FormRow label="Description">
            <input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-[55vw] max-w-[220px] bg-transparent text-right text-[15px] outline-none"
              style={{ color: C.text }}
            />
          </FormRow>
          <FormRow label="Date">
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="bg-transparent text-right text-[15px] tabular-nums outline-none"
              style={{ color: C.text }}
            />
          </FormRow>
          <FormRow label="Category" chevron onClick={() => setCategoryPickerOpen(true)}>
            <span style={{ color: C.text }}>
              {cat?.label ?? "Uncategorized"}
            </span>
          </FormRow>
        </div>

        <div className="mx-4 mt-3 rounded-[14px] p-4" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
          <div className="mb-1.5 text-[13px]" style={{ color: C.muted }}>
            Note (optional)
          </div>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value.slice(0, 500))}
            placeholder="team lunch, reimbursable, …"
            className="min-h-[64px] w-full resize-none bg-transparent text-[14px] leading-[1.5] outline-none"
            style={{ color: C.text }}
          />
        </div>

        <div className="px-5 pt-8">
          <GoldButton onClick={() => router.back()}>Save changes</GoldButton>
        </div>

        <PickerSheet
          open={categoryPickerOpen}
          title="Category"
          items={categories}
          selectedId={categoryId}
          onSelect={setCategoryId}
          onClose={() => setCategoryPickerOpen(false)}
        />
      </main>
    </PageTransition>
  );
}
