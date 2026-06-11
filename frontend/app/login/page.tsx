"use client";

import { AuthForm } from "@/components/auth/auth-form";
import { login } from "@/lib/api";

export default function LoginPage() {
  return <AuthForm mode="login" action={login} />;
}
