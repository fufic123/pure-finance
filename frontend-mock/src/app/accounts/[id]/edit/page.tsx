"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MOCK_ACCOUNTS } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { TopBar } from "@/components/top-bar";
import { GoldButton } from "@/components/gold-button";
import { FormRow } from "@/components/form-row";

export default function EditAccountPage() {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);
  const acc = MOCK_ACCOUNTS[0]!;

  const [name, setName] = useState(acc.name);
  const [balance, setBalance] = useState(acc.balance.replace(",", ""));

  return (
    <PageTransition>
      <main className="min-h-screen pb-10" style={{ background: C.bg }}>
        <TopBar title="Edit account" back />

        <div className="mx-4 mt-3 overflow-hidden rounded-[14px]" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
          <FormRow label="Institution">
            <span style={{ color: C.muted }}>{acc.name}</span>
          </FormRow>
          <FormRow label="Name">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-[55vw] max-w-[220px] bg-transparent text-right text-[15px] outline-none"
              style={{ color: C.text }}
            />
          </FormRow>
          <FormRow label="Currency">
            <span style={{ color: C.muted }}>{acc.currency}</span>
          </FormRow>
          <FormRow label="Balance">
            <div className="flex items-center gap-1">
              <span style={{ color: C.muted }}>€</span>
              <input
                inputMode="decimal"
                value={balance}
                onChange={(e) => setBalance(e.target.value)}
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
          Changing the balance appends a snapshot — history is kept.
        </p>

        <div className="px-5 pt-8">
          <GoldButton onClick={() => router.back()}>Save changes</GoldButton>
        </div>
      </main>
    </PageTransition>
  );
}
