"use client";

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { BrandMark } from "@/components/brand-mark";
import { GoldButton } from "@/components/gold-button";
import { PageTransition } from "@/components/page-transition";

export default function Landing() {
  const router = useRouter();

  return (
    <PageTransition>
      <main className="pf-safe-top pf-safe-bottom flex min-h-screen flex-col bg-pf-black">
        <div className="flex flex-1 flex-col items-center justify-center gap-5 px-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.35, ease: "easeOut", delay: 0.05 }}
          >
            <BrandMark />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: "easeOut", delay: 0.15 }}
            className="flex flex-col items-center gap-2 text-center"
          >
            <div className="flex items-center gap-2">
              <span className="text-[26px] font-medium tracking-tight text-pf-white">Pure</span>
              <span className="pf-gold-text text-[26px] font-medium">·</span>
              <span className="text-[26px] font-medium tracking-tight text-pf-white">Finance</span>
            </div>
            <p className="text-[15px] text-white/40">All your money, one clean view.</p>
          </motion.div>
        </div>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: "easeOut", delay: 0.25 }}
          className="px-5 pb-10"
        >
          <GoldButton onClick={() => router.push("/home")}>Continue with Google</GoldButton>
          <p className="mt-3 text-center text-[12px] text-white/25">Your data stays yours.</p>
        </motion.div>
      </main>
    </PageTransition>
  );
}
