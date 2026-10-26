import type { ReactNode } from "react";

import { ChoiceButton } from "../atoms/buttons";
import { Fieldset } from "../atoms/Fieldset";

export interface Choice<T extends string> {
  readonly value: T;
  readonly label: string;
}

interface ChoiceGroupProps<T extends string> {
  readonly legend: string;
  readonly choices: readonly Choice<T>[];
  readonly chosen: T;
  readonly onChoose: (value: T) => void;
  // Ce qui complète les choix, sous eux.
  readonly children?: ReactNode;
}

// Une question à réponse unique : un seul choix est fait à la fois.
export function ChoiceGroup<T extends string>({
  legend,
  choices,
  chosen,
  onChoose,
  children,
}: ChoiceGroupProps<T>) {
  return (
    <Fieldset legend={legend}>
      <div className="flex flex-wrap gap-2">
        {choices.map(({ value, label }) => (
          <ChoiceButton
            key={value}
            pressed={value === chosen}
            onClick={() => {
              onChoose(value);
            }}
          >
            {label}
          </ChoiceButton>
        ))}
      </div>
      {children}
    </Fieldset>
  );
}
