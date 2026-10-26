import type { ReactNode } from "react";

interface EyebrowProps {
  readonly children: ReactNode;
  // Collé à ce qui le suit, dans un en-tête ou une réponse.
  readonly flush?: boolean;
}

// Le surtitre en petites capitales, au-dessus d'un titre.
export function Eyebrow({ children, flush = false }: EyebrowProps) {
  return (
    <p
      className={`${flush ? "mb-0" : "mb-2"} text-[13px] font-medium tracking-[0.08em] text-text-muted uppercase`}
    >
      {children}
    </p>
  );
}
