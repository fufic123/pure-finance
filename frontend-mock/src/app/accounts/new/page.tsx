"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MOCK_INSTITUTIONS } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { TopBar } from "@/components/top-bar";
import { GoldButton } from "@/components/gold-button";
import { FormRow } from "@/components/form-row";
import { PickerSheet } from "@/components/picker-sheet";

export default function NewAccountPage() {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);

  const [institutionId, setInstitutionId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [balance, setBalance] = useState("");
  const [pickerOpen, setPickerOpen] = useState(false);

  const inst = MOCK_INSTITUTIONS.find((i) => i.id === institutionId);

  return (
    <PageTransition>
      <main className="min-h-screen pb-10" style={{ background: C.bg }}>
        <TopBar title="Add account" back />

        <div className="mx-4 mt-3 overflow-hidden rounded-[14px]" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
          <FormRow label="Institution" chevron onClick={() => setPickerOpen(true)}>
            <span style={{ color: inst ? C.text : C.muted }}>
              {inst?.name ?? "Select bank"}
            </span>
          </FormRow>
          <FormRow label="Name">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Main Revolut"
              className="w-[55vw] max-w-[220px] bg-transparent text-right text-[15px] outline-none"
              style={{ color: C.text }}
            />
          </FormRow>
          <FormRow label="Currency">
            <span style={{ color: C.muted }}>EUR</span>
          </FormRow>
          <FormRow label="Initial balance">
            <div className="flex items-center gap-1">
              <span style={{ color: C.muted }}>€</span>
              <input
                inputMode="decimal"
                value={balance}
                onChange={(e) => setBalance(e.target.value)}
                placeholder="0.00"
                className="w-[40vw] max-w-[160px] bg-transparent text-right text-[15px] tabular-nums outline-none"
                style={{ color: C.text }}
              />
            </div>
          </FormRow>
        </div>

        <p
          className="mx-5 mt-3 text-[12px] leading-[1.45]"
          style={{ color: C.muted }}
        >
          Currency is EUR only for now. Multi-currency support is on the roadmap.
        </p>

        <div className="px-5 pt-8">
          <GoldButton onClick={() => router.back()}>Add account</GoldButton>
        </div>

        <PickerSheet
          open={pickerOpen}
          title="Institution"
          items={MOCK_INSTITUTIONS.map((i) => ({ id: i.id, label: i.name }))}
          selectedId={institutionId}
          onSelect={setInstitutionId}
          onClose={() => setPickerOpen(false)}
        />
      </main>
    </PageTransition>
  );
}
