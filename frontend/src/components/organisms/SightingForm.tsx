import { ErrorText } from "../atoms/ErrorText";
import { PrimaryButton } from "../atoms/buttons";
import { ChoiceGroup, type Choice } from "../molecules/ChoiceGroup";
import { EarlierTimeField } from "../molecules/EarlierTimeField";
import { DirectionPicker, type DirectionPickerProps } from "./DirectionPicker";
import type { SightingMoment } from "../../lib/sighting";

const MOMENTS: readonly Choice<SightingMoment>[] = [
  { value: "now", label: "À l'instant" },
  { value: "fifteen-minutes-ago", label: "Il y a 15 min" },
  { value: "earlier", label: "Plus tôt" },
];

export interface SightingFormProps {
  readonly moment: SightingMoment;
  readonly onMoment: (moment: SightingMoment) => void;
  readonly earlier: string;
  readonly onEarlier: (earlier: string) => void;
  readonly direction: DirectionPickerProps;
  readonly alert: string;
  readonly busy: boolean;
  readonly onSubmit: () => void;
}

// Quand et dans quelle direction le visiteur a vu sa lumière ; la page vérifie le reste.
export function SightingForm({
  moment,
  onMoment,
  earlier,
  onEarlier,
  direction,
  alert,
  busy,
  onSubmit,
}: SightingFormProps) {
  return (
    <form
      noValidate
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <ChoiceGroup legend="Quand ?" choices={MOMENTS} chosen={moment} onChoose={onMoment}>
        <EarlierTimeField value={earlier} onChange={onEarlier} hidden={moment !== "earlier"} />
      </ChoiceGroup>
      <DirectionPicker {...direction} />
      <ErrorText>{alert}</ErrorText>
      <PrimaryButton busy={busy}>Identifier</PrimaryButton>
    </form>
  );
}
