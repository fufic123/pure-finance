"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { MOCK_ACCOUNTS, MOCK_CATEGORY_TREE } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { TopBar } from "@/components/top-bar";
import { GoldButton } from "@/components/gold-button";
import { FormRow } from "@/components/form-row";
import { PickerSheet, type PickerItem } from "@/components/picker-sheet";
import { SegmentedControl } from "@/components/segmented-control";

type TxType = "expense" | "income";

const TYPE_OPTIONS = [
  { value: "expense" as TxType, label: "Expense" },
  { value: "income" as TxType, label: "Income" },
] as const;

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

function todayIso(): string {
  const d = new Date();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${mm}-${dd}`;
}

export default function NewTransactionPage() {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);

  const categories = useMemo(flattenCategories, []);
  const [type, setType] = useState<TxType>("expense");
  const [accountId, setAccountId] = useState<string | null>(MOCK_ACCOUNTS[0]?.id ?? null);
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState(todayIso());
  const [categoryId, setCategoryId] = useState<string | null>("");
  const [note, setNote] = useState("");
  const [accountPickerOpen, setAccountPickerOpen] = useState(false);
  const [categoryPickerOpen, setCategoryPickerOpen] = useState(false);

  const acc = MOCK_ACCOUNTS.find((a) => a.id === accountId);
  const cat = categories.find((c) => c.id === categoryId);

  return (
    <PageTransition>
      <main className="min-h-screen pb-10" style={{ background: C.bg }}>
        <TopBar title="Add transaction" back />

        <div className="px-4 pt-3">
          <SegmentedControl options={TYPE_OPTIONS} value={type} onChange={setType} />
        </div>

        <div className="mx-4 mt-3 overflow-hidden rounded-[14px]" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
          <FormRow label="Account" chevron onClick={() => setAccountPickerOpen(true)}>
            <span style={{ color: acc ? C.text : C.muted }}>
              {acc?.name ?? "Select account"}
            </span>
          </FormRow>
          <FormRow label="Amount">
            <div className="flex items-center gap-1">
              <span style={{ color: C.muted }}>
                {type === "expense" ? "−€" : "+€"}
              </span>
              <input
                inputMode="decimal"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="w-[35vw] max-w-[140px] bg-transparent text-right text-[15px] tabular-nums outline-none"
                style={{ color: C.text }}
              />
            </div>
          </FormRow>
          <FormRow label="Description">
            <input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="e.g. Bolt Food"
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
          <GoldButton onClick={() => router.back()}>Add transaction</GoldButton>
        </div>

        <PickerSheet
          open={accountPickerOpen}
          title="Account"
          items={MOCK_ACCOUNTS.map((a) => ({ id: a.id, label: a.name, sublabel: `€${a.balance}` }))}
          selectedId={accountId}
          onSelect={setAccountId}
          onClose={() => setAccountPickerOpen(false)}
        />
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
