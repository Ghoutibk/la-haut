import type { ReactNode } from "react";

// Une phrase d'une réponse ou d'un remerciement.
export function Sentence({ children }: { readonly children: ReactNode }) {
  return <p className="mb-1.5 text-text-soft">{children}</p>;
}
