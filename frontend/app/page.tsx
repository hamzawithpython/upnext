import { Navbar } from "@/components/marketing/navbar";
import { Hero } from "@/components/marketing/hero";
import { Features } from "@/components/marketing/features";
import { HowItWorks } from "@/components/marketing/how-it-works";
import { Waitlist } from "@/components/marketing/waitlist";
import { Footer } from "@/components/marketing/footer";

export default function Home() {
  return (
    <main className="relative">
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <Waitlist />
      <Footer />
    </main>
  );
}
