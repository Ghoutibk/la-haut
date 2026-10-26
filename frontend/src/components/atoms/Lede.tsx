import type { ReactNode } from "react";

interface LedeProps {
  readonly children: ReactNode;
  // Ce que la vue annonce d'elle-même : le lecteur d'écran le lit quand il change.
  readonly announces?: boolean;
}

// Le chapeau sous un titre.
export function Lede({ children, announces = false }: LedeProps) {
  return (
    <p className="mb-5 text-text-soft" role={announces ? "status" : undefined}>
      {children}
    </p>
  );
}
