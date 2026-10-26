import type { ReactNode } from "react";

// Sous le doigt, le bouton se tasse un instant, sauf si le visiteur préfère réduire les animations.
const PRESS =
  "cursor-pointer transition-[scale,background-color] duration-120 ease-out motion-safe:active:scale-97";

interface ButtonProps {
  readonly children: ReactNode;
  readonly onClick: () => void;
}

const CHOICE_SHAPES = {
  pill: "rounded-full px-4",
  rose: "rounded-[14px] px-0",
  full: "w-full rounded-full px-4",
} as const;

interface ChoiceButtonProps extends ButtonProps {
  // Fait ou non, pour un choix d'un groupe ; absent pour un bouton seul.
  readonly pressed?: boolean;
  readonly shape?: keyof typeof CHOICE_SHAPES;
  // Le nom en toutes lettres d'un choix abrégé.
  readonly label?: string;
}

export function ChoiceButton({
  children,
  onClick,
  pressed,
  shape = "pill",
  label,
}: ChoiceButtonProps) {
  return (
    <button
      type="button"
      className={`${PRESS} ${CHOICE_SHAPES[shape]} min-h-11 border border-line bg-surface text-[15px] text-text aria-pressed:border-accent aria-pressed:bg-accent aria-pressed:font-semibold aria-pressed:text-on-accent`}
      aria-pressed={pressed}
      aria-label={label}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

interface PrimaryButtonProps {
  readonly children: ReactNode;
  // Là-haut travaille : le bouton patiente.
  readonly busy: boolean;
}

// Le bouton qui envoie le formulaire où il est posé.
export function PrimaryButton({ children, busy }: PrimaryButtonProps) {
  return (
    <button
      type="submit"
      className={`${PRESS} min-h-14 w-full rounded-2xl border-0 bg-accent text-[17px] font-semibold text-on-accent aria-busy:cursor-progress aria-busy:opacity-70`}
      aria-busy={busy ? true : undefined}
    >
      {children}
    </button>
  );
}

export function OutlineButton({ children, onClick }: ButtonProps) {
  return (
    <button
      type="button"
      className="mb-3 flex min-h-13 w-full cursor-pointer items-center justify-center gap-2 rounded-2xl border border-accent bg-transparent text-base font-semibold text-accent"
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export function LinkButton({ children, onClick }: ButtonProps) {
  return (
    <button
      type="button"
      className="cursor-pointer border-0 bg-transparent p-0 text-sky-blue underline"
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export function CloseButton({ onClick }: { readonly onClick: () => void }) {
  return (
    <button
      type="button"
      className="size-9 cursor-pointer rounded-full border border-line bg-surface text-[22px] leading-none text-text-soft"
      aria-label="Fermer"
      onClick={onClick}
    >
      ×
    </button>
  );
}
