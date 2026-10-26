import { DateTimeInput } from "../atoms/inputs";
import { Field } from "../atoms/Field";

interface EarlierTimeFieldProps {
  readonly value: string;
  readonly onChange: (value: string) => void;
  readonly hidden: boolean;
}

// L'heure d'une lumière vue « Plus tôt », à l'heure du visiteur.
export function EarlierTimeField({ value, onChange, hidden }: EarlierTimeFieldProps) {
  return (
    <Field label="Heure à laquelle tu l'as vue" hidden={hidden}>
      <DateTimeInput value={value} onChange={onChange} />
    </Field>
  );
}
