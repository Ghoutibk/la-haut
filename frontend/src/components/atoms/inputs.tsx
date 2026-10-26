// Les champs que le visiteur remplit : leur valeur vient de la page, chaque frappe y retourne.

const FIELD = "min-h-11 rounded-xl border border-line bg-surface px-3 text-text";

interface InputProps {
  readonly value: string;
  readonly onChange: (value: string) => void;
}

interface TextAreaProps extends InputProps {
  readonly maxLength: number;
  readonly placeholder: string;
}

export function TextArea({ value, onChange, maxLength, placeholder }: TextAreaProps) {
  return (
    <textarea
      className={`${FIELD} min-h-30 resize-y py-2.5`}
      rows={5}
      maxLength={maxLength}
      placeholder={placeholder}
      value={value}
      onChange={(event) => {
        onChange(event.target.value);
      }}
    />
  );
}

export function EmailInput({
  value,
  onChange,
  maxLength,
}: InputProps & { readonly maxLength: number }) {
  return (
    <input
      type="email"
      className={FIELD}
      autoComplete="email"
      maxLength={maxLength}
      value={value}
      onChange={(event) => {
        onChange(event.target.value);
      }}
    />
  );
}

export function DateTimeInput({ value, onChange }: InputProps) {
  return (
    <input
      type="datetime-local"
      className={FIELD}
      value={value}
      onChange={(event) => {
        onChange(event.target.value);
      }}
    />
  );
}
