"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getCurrentUser, getPreferences, type Preferences } from "@/lib/api";
import { OnboardingFlow } from "@/components/onboarding/onboarding-flow";

export default function OnboardingPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [existing, setExisting] = useState<Preferences | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      const user = await getCurrentUser();
      if (!active) return;
      if (!user) {
        router.replace("/login");
        return;
      }
      // Load any existing preferences so the flow can pre-fill them (edit mode).
      // We intentionally do NOT auto-skip onboarded users — this page doubles as
      // "Edit interests". The dashboard layout guard handles un-onboarded users.
      const prefs = await getPreferences();
      if (!active) return;
      setExisting(prefs);
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

  return <OnboardingFlow existing={existing} />;
}
