import { ChoiceButton } from "../atoms/buttons";

interface AimingPanelProps {
  // Ce que la page dit de la visée : la lecture en cours, puis le point visé.
  readonly reading: string;
  readonly onDone: () => void;
}

// Pendant la visée, la rose suit le téléphone jusqu'à « C'est là ».
export function AimingPanel({ reading, onDone }: AimingPanelProps) {
  return (
    <div className="mb-3 rounded-2xl border border-line bg-surface-deep px-4 py-3.5">
      <p className="mb-2 text-sm text-text-soft">
        Tiens ton téléphone à plat devant toi et tourne-toi : le haut de l'écran doit pointer vers
        l'endroit où tu as vu la lumière.
      </p>
      <p className="mb-3 font-serif text-[28px] leading-[1.2]" role="status">
        {reading}
      </p>
      <ChoiceButton shape="full" onClick={onDone}>
        C'est là
      </ChoiceButton>
    </div>
  );
}
