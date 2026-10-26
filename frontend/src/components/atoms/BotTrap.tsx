interface BotTrapProps {
  readonly value: string;
  readonly onChange: (value: string) => void;
}

// Piège à robots : hors de l'écran pour les humains, rempli par les robots qui lisent le code.
export function BotTrap({ value, onChange }: BotTrapProps) {
  return (
    <div className="absolute -left-[10000px] h-px w-px overflow-hidden" aria-hidden="true">
      <label>
        Ne remplis pas ce champ{" "}
        <input
          type="text"
          tabIndex={-1}
          autoComplete="off"
          value={value}
          onChange={(event) => {
            onChange(event.target.value);
          }}
        />
      </label>
    </div>
  );
}
