import { Hero } from "@/components/sections/Hero";
import { Curriculum } from "@/components/sections/Curriculum";
import { Compare } from "@/components/sections/Compare";
import { CallToAction } from "@/components/sections/CallToAction";

export default function HomePage() {
  return (
    <>
      <Hero />
      <Curriculum />
      <Compare />
      <CallToAction />
    </>
  );
}
