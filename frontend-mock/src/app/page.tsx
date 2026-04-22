"use client";

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { BrandMark } from "@/components/brand-mark";
import { SignInButton } from "@/components/sign-in-button";
import { PageTransition } from "@/components/page-transition";
import { GOLD_TEXT_STYLE, pfTheme } from "@/lib/tokens";
import { useTheme } from "@/lib/theme";

export default function Landing() {
  const router = useRouter();
  const { dark } = useTheme();
  const C = pfTheme(dark);

  return (
    <PageTransition>
      <main
        className="pf-safe-top pf-safe-bottom flex min-h-screen flex-col px-6"
        style={{ background: C.bg }}
      >
        <div style={{ height: 62 }} />

        {/* Small wordmark */}
        <motion.div
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: "easeOut", delay: 0.05 }}
          className="mb-16"
        >
          <BrandMark dark={dark} />
        </motion.div>

        {/* Large headline */}
        <div className="flex flex-1 flex-col justify-center">
          <motion.h1
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease: "easeOut", delay: 0.1 }}
            className="m-0 mb-4"
            style={{
              fontSize: 38,
              fontWeight: 600,
              color: C.text,
              lineHeight: 1.1,
              letterSpacing: "-1.2px",
            }}
          >
            All your
            <br />
            money,
            <br />
            <span
              style={{
                ...GOLD_TEXT_STYLE,
                fontSize: 38,
                fontWeight: 600,
                letterSpacing: "-1.2px",
                lineHeight: 1.1,
              }}
            >
              one clear
              <br />
              view.
            </span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease: "easeOut", delay: 0.18 }}
            className="m-0"
            style={{ fontSize: 16, color: C.muted, lineHeight: 1.5 }}
          >
            Connect your banks. Track what matters.
            <br />
            No clutter, no noise.
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: "easeOut", delay: 0.25 }}
          className="pb-10"
        >
          <SignInButton dark={dark} onClick={() => router.push("/onboarding")}>
            Continue with Google
          </SignInButton>
          <p
            className="mt-3 text-center text-[12px]"
            style={{ color: C.muted }}
          >
            Your data stays yours.
          </p>
        </motion.div>
      </main>
    </PageTransition>
  );
}
