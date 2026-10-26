import type { ReactNode } from "react";

// L'alerte d'un formulaire : toujours en place, même vide, pour que le lecteur d'écran la suive.
export function ErrorText({ children }: { readonly children: ReactNode }) {
  return (
    <p className="mb-2 min-h-[1.5em] text-sm text-error" role="alert">
      {children}
    </p>
  );
}
