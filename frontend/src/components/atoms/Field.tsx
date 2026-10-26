import type { ReactNode } from "react";

interface FieldProps {
  readonly label: string;
  readonly children: ReactNode;
  readonly hidden?: boolean;
}

// Un champ et son libellé : le libellé l'enveloppe, et le nomme ainsi.
export function Field({ label, children, hidden = false }: FieldProps) {
  return (
    <label className="mt-3 grid gap-1.5 text-sm text-text-soft" hidden={hidden}>
      <span>{label}</span>
      {children}
    </label>
  );
}
