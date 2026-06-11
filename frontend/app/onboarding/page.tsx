"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getCurrentUser, getPreferences } from "@/lib/api";
import { OnboardingFlow } from "@/components/onboarding/onboarding-flow";

export default function OnboardingPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let active = true;
    (async () => {
      const user = await getCurrentUser();
      if (!active) return;
      if (!user) {
        router.replace("/login");
        return;
      }
      // If already onboarded, skip straight to the dashboard.
      const prefs = await getPreferences();
      if (!active) return;
      if (prefs?.onboarded) {
        router.replace("/dashboard");
        return;
      }
      setReady(true);
    })();
    return () => {
      active = false;
    };
  }, [router]);

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-border border-t-brand" />
      </div>
    );
  }

  return <OnboardingFlow />;
}
