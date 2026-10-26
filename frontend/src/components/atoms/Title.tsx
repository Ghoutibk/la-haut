import type { ReactNode } from "react";

interface TitleProps {
  readonly children: ReactNode;
  // 1 pour le titre d'une vue, 2 pour celui d'une fenêtre ou d'une réponse.
  readonly level: 1 | 2;
  readonly id?: string;
  // Dans la couleur de l'accent, comme le nom d'une réponse.
  readonly accent?: boolean;
}

export function Title({ children, level, id, accent = false }: TitleProps) {
  if (level === 1) {
    return (
      <h1
        id={id}
        className="mb-3 font-serif text-[clamp(32px,9vw,40px)] leading-[1.05] font-normal"
      >
        {children}
      </h1>
    );
  }
  return (
    <h2
      id={id}
      className={`mt-1 mb-2 font-serif text-[32px] leading-[1.05] font-normal ${accent ? "text-accent" : ""}`}
    >
      {children}
    </h2>
  );
}
