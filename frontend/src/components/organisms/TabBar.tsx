import type { ReactNode } from "react";

import { MoonIcon, TargetIcon } from "../atoms/icons";
import { TabLink } from "../molecules/TabLink";
import type { View } from "../../lib/route";

const TABS: readonly { view: View; label: string; icon: ReactNode }[] = [
  { view: "tonight", label: "Ce soir", icon: <MoonIcon /> },
  { view: "sighting", label: "C'était quoi ?", icon: <TargetIcon /> },
];

interface TabBarProps {
  readonly anchors: Readonly<Record<View, string>>;
  readonly current: View;
}

// Les onglets, en bas de l'écran comme sur un téléphone.
export function TabBar({ anchors, current }: TabBarProps) {
  return (
    <nav
      className="fixed inset-x-0 bottom-0 mx-auto grid max-w-120 grid-cols-2 border-t border-line-soft bg-surface-deep pt-1.5 pb-[max(10px,env(safe-area-inset-bottom))]"
      aria-label="Navigation principale"
    >
      {TABS.map(({ view, label, icon }) => (
        <TabLink
          key={view}
          href={anchors[view]}
          label={label}
          icon={icon}
          current={view === current}
        />
      ))}
    </nav>
  );
}
