import type { ReactNode } from "react";

interface TabLinkProps {
  // L'ancre de la vue.
  readonly href: string;
  readonly label: string;
  readonly icon: ReactNode;
  // C'est la vue affichée.
  readonly current: boolean;
}

export function TabLink({ href, label, icon, current }: TabLinkProps) {
  return (
    <a
      href={href}
      className="flex min-h-[50px] flex-col items-center justify-center gap-1 text-xs text-text-muted no-underline aria-[current=page]:font-semibold aria-[current=page]:text-accent"
      aria-current={current ? "page" : undefined}
    >
      {icon}
      <span>{label}</span>
    </a>
  );
}
