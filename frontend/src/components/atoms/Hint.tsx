import type { ReactNode } from "react";

// Une précision discrète sous un champ ou un groupe de choix.
export function Hint({ children }: { readonly children: ReactNode }) {
  return <p className="mt-2.5 text-[13px] text-text-muted">{children}</p>;
}
