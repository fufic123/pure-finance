"use client";

import { useEffect, useState } from "react";
import { GoldButton } from "@/components/gold-button";
import { getCurrentUser, logout, startGoogleAuth } from "@/lib/api/auth";
import { tokenStorage } from "@/lib/auth/storage";
import type { User } from "@/lib/api/types";

export default function Landing() {
  const [checking, setChecking] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [signingIn, setSigningIn] = useState(false);

  useEffect(() => {
    if (!tokenStorage.getRefresh()) {
      setChecking(false);
      return;
    }
    getCurrentUser()
      .then(setUser)
      .catch(() => tokenStorage.clear())
      .finally(() => setChecking(false));
  }, []);

  async function signIn() {
    setError(null);
    setSigningIn(true);
    try {
      const redirectUri = `${window.location.origin}/auth/callback`;
      const url = await startGoogleAuth(redirectUri);
      window.location.assign(url);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Sign-in failed");
      setSigningIn(false);
    }
  }

  async function signOut() {
    await logout();
    setUser(null);
  }

  if (checking) return <SplashScreen />;
  if (user) return <SignedInPlaceholder user={user} onSignOut={signOut} />;
  return <SignInScreen onSignIn={signIn} signingIn={signingIn} error={error} />;
}

function SplashScreen() {
  return (
    <main className="pf-safe-top pf-safe-bottom flex min-h-screen items-center justify-center bg-pf-black">
      <BrandMark />
    </main>
  );
}

function SignInScreen({
  onSignIn,
  signingIn,
  error,
}: {
  onSignIn: () => void;
  signingIn: boolean;
  error: string | null;
}) {
  return (
    <main className="pf-safe-top pf-safe-bottom flex min-h-screen flex-col bg-pf-black">
      <div className="flex flex-1 flex-col items-center justify-center gap-5 px-6">
        <BrandMark />
        <div className="flex flex-col items-center gap-2 text-center">
          <div className="flex items-center gap-2">
            <span className="text-[26px] font-medium tracking-tight text-pf-white">Pure</span>
            <span className="pf-gold-text text-[26px] font-medium">·</span>
            <span className="text-[26px] font-medium tracking-tight text-pf-white">Finance</span>
          </div>
          <p className="text-[15px] text-white/40">All your money, one clean view.</p>
        </div>
      </div>
      <div className="px-5 pb-10">
        <GoldButton onClick={onSignIn} disabled={signingIn}>
          {signingIn ? "Redirecting…" : "Continue with Google"}
        </GoldButton>
        {error ? (
          <p className="mt-3 text-center text-[13px] text-pf-expense">{error}</p>
        ) : (
          <p className="mt-3 text-center text-[12px] text-white/25">Your data stays yours.</p>
        )}
      </div>
    </main>
  );
}

function SignedInPlaceholder({ user, onSignOut }: { user: User; onSignOut: () => void }) {
  return (
    <main className="pf-safe-top pf-safe-bottom flex min-h-screen flex-col items-center justify-center gap-4 bg-pf-black px-6">
      <BrandMark />
      <p className="text-[15px] text-white/60">Signed in as</p>
      <p className="pf-gold-text text-lg font-medium">{user.email}</p>
      <button
        type="button"
        onClick={onSignOut}
        className="mt-4 text-[13px] text-white/40 underline-offset-4 hover:underline"
      >
        Sign out
      </button>
      <p className="mt-8 text-center text-[12px] text-white/25">
        Home screen coming in the next task.
      </p>
    </main>
  );
}

function BrandMark() {
  return (
    <div
      className="flex h-[72px] w-[72px] items-center justify-center rounded-2xl"
      style={{ background: "#0A0A0A", boxShadow: "inset 0 0 0 1px #1F1F1F" }}
    >
      <div className="h-9 w-[3px] rounded-[2px] bg-gold-metallic" />
    </div>
  );
}
