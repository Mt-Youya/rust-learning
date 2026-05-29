"use client";

import dynamic from "next/dynamic";

// ssr: false is only valid in Client Components
const OwnershipScene = dynamic(
  () => import("./OwnershipScene").then((m) => m.OwnershipScene),
  {
    ssr: false,
    loading: () => <div className="absolute inset-0" />,
  }
);

export function OwnershipSceneClient({ className }: { className?: string }) {
  return <OwnershipScene className={className} />;
}
