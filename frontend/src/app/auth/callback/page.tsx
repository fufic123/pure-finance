"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useRef, useState } from "react";
import { completeGoogleAuth } from "@/lib/api/auth";

export default function Callback() {
  return (
    <Suspense fallback={<CallbackFrame message="Completing sign-in…" />}>
      <CallbackInner />
    </Suspense>
  );
}

function CallbackInner() {
  const router = useRouter();
  const params = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const exchangedCode = useRef<string | null>(null);

  useEffect(() => {
    const code = params.get("code");
    const state = params.get("state");
    const googleError = params.get("error");

    if (googleError) {
      setError(googleError);
      return;
    }
    if (!code || !state) {
      setError("Missing code or state from Google");
      return;
    }
    if (exchangedCode.current === code) return;
    exchangedCode.current = code;

    const redirectUri = `${window.location.origin}/auth/callback`;
    completeGoogleAuth(code, redirectUri, state)
      .then(() => router.replace("/"))
      .catch((e) => setError(e instanceof Error ? e.message : "Sign-in failed"));
  }, [params, router]);

  if (error) {
    return (
      <CallbackFrame message="Sign-in failed">
        <p className="text-center text-[13px] text-pf-expense">{error}</p>
        <Link
          href="/"
          replace
          className="text-[14px] text-white/60 underline-offset-4 hover:underline"
        >
          Try again
        </Link>
      </CallbackFrame>
    );
  }
  return <CallbackFrame message="Completing sign-in…" />;
}

function CallbackFrame({ message, children }: { message: string; children?: React.ReactNode }) {
  return (
    <main className="pf-safe-top pf-safe-bottom flex min-h-screen flex-col items-center justify-center gap-4 bg-pf-black px-6">
      <div
        className="flex h-[72px] w-[72px] items-center justify-center rounded-2xl"
        style={{ background: "#0A0A0A", boxShadow: "inset 0 0 0 1px #1F1F1F" }}
      >
        <div className="h-9 w-[3px] rounded-[2px] bg-gold-metallic" />
      </div>
      <p className="text-[15px] text-white/60">{message}</p>
      {children}
    </main>
  );
}
