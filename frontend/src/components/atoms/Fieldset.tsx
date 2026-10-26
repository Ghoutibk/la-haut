import type { ReactNode } from "react";

interface FieldsetProps {
  readonly legend: string;
  readonly children: ReactNode;
}

// Une question du formulaire : sa légende nomme le groupe des réponses.
export function Fieldset({ legend, children }: FieldsetProps) {
  return (
    <fieldset className="mb-5.5 border-0 p-0">
      <legend className="mb-2.5 p-0 font-medium">{legend}</legend>
      {children}
    </fieldset>
  );
}
