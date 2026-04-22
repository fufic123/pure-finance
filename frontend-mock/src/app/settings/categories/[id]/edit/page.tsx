"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { MOCK_CATEGORY_TREE } from "@/lib/mock";
import { pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";
import { PageTransition } from "@/components/page-transition";
import { TopBar } from "@/components/top-bar";
import { GoldButton } from "@/components/gold-button";
import { FormRow } from "@/components/form-row";
import { PickerSheet } from "@/components/picker-sheet";

export default function EditCategoryPage() {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);

  // Mock: first user-created child across the tree
  const seed =
    MOCK_CATEGORY_TREE[0]?.children.find((c) => !c.system) ??
    MOCK_CATEGORY_TREE[0]!.children[0]!;

  const [name, setName] = useState(seed.name);
  const [parentId, setParentId] = useState<string | null>(MOCK_CATEGORY_TREE[0]!.id);
  const [pickerOpen, setPickerOpen] = useState(false);

  const parentItems = [
    { id: "", label: "Top-level (no parent)" },
    ...MOCK_CATEGORY_TREE.map((p) => ({ id: p.id, label: p.name })),
  ];
  const parent = parentItems.find((p) => p.id === parentId);

  return (
    <PageTransition>
      <main className="min-h-screen pb-10" style={{ background: C.bg }}>
        <TopBar title="Edit category" back />

        <div className="mx-4 mt-3 overflow-hidden rounded-[14px]" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
          <FormRow label="Name">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-[55vw] max-w-[220px] bg-transparent text-right text-[15px] outline-none"
              style={{ color: C.text }}
            />
          </FormRow>
          <FormRow label="Parent" chevron onClick={() => setPickerOpen(true)}>
            <span style={{ color: C.text }}>{parent?.label ?? "Top-level"}</span>
          </FormRow>
        </div>

        <div className="px-5 pt-8">
          <GoldButton onClick={() => router.back()}>Save changes</GoldButton>
        </div>

        <PickerSheet
          open={pickerOpen}
          title="Parent category"
          items={parentItems}
          selectedId={parentId}
          onSelect={setParentId}
          onClose={() => setPickerOpen(false)}
        />
      </main>
    </PageTransition>
  );
}
