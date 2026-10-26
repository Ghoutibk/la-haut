import type { ReactNode } from "react";

const CHIP =
  "inline-flex h-8 items-center gap-1.5 rounded-full bg-surface px-3 text-[13px] text-text-soft";

// Une pastille de l'en-tête : un renseignement, ou un bouton discret.
export function Chip({ children }: { readonly children: ReactNode }) {
  return <span className={CHIP}>{children}</span>;
}

interface ChipButtonProps {
  readonly children: ReactNode;
  readonly onClick: () => void;
  // La puce ouvre une fenêtre posée sur la page.
  readonly opensDialog?: boolean;
}

export function ChipButton({ children, onClick, opensDialog = false }: ChipButtonProps) {
  return (
    <button
      type="button"
      className={`${CHIP} cursor-pointer border-0 font-[inherit]`}
      aria-haspopup={opensDialog ? "dialog" : undefined}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
