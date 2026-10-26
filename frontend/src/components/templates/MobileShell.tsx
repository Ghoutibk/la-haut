import type { ReactNode } from "react";

import { FeedbackDialog, type FeedbackDialogProps } from "../organisms/FeedbackDialog";
import { TabBar, type TabBarProps } from "../organisms/TabBar";
import { TopBar, type TopBarProps } from "../organisms/TopBar";

interface MobileShellProps {
  readonly topBar: TopBarProps;
  readonly tabBar: TabBarProps;
  readonly feedback: FeedbackDialogProps;
  // Les vues de la page.
  readonly children: ReactNode;
}

// La page tient dans la largeur d'un téléphone, entre l'en-tête et les onglets du bas.
export function MobileShell({ topBar, tabBar, feedback, children }: MobileShellProps) {
  return (
    <div className="mx-auto min-h-dvh max-w-120 px-4 pt-[max(20px,env(safe-area-inset-top))] pb-[calc(var(--tabs-height)+32px+env(safe-area-inset-bottom))]">
      <TopBar {...topBar} />
      <main>{children}</main>
      <TabBar {...tabBar} />
      <FeedbackDialog {...feedback} />
    </div>
  );
}
