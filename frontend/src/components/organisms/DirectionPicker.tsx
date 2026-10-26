import { Fieldset } from "../atoms/Fieldset";
import { Hint } from "../atoms/Hint";
import { AimButton } from "../molecules/AimButton";
import { AimingPanel } from "../molecules/AimingPanel";
import { CompassRose } from "../molecules/CompassRose";
import type { CompassPoint, RoseLayout } from "../../lib/compass";

export interface AimingProps {
  // Le téléphone a une boussole et un écran tactile.
  readonly available: boolean;
  readonly active: boolean;
  readonly reading: string;
  readonly onStart: () => void;
  readonly onDone: () => void;
}

export interface DirectionPickerProps {
  readonly rose: RoseLayout;
  readonly chosen: CompassPoint | null;
  readonly onChoose: (point: CompassPoint) => void;
  readonly aiming: AimingProps;
}

// « Dans quelle direction ? » : viser avec le téléphone, ou choisir sur la rose des vents.
export function DirectionPicker({ rose, chosen, onChoose, aiming }: DirectionPickerProps) {
  return (
    <Fieldset legend="Dans quelle direction ?">
      {aiming.available && !aiming.active && <AimButton onClick={aiming.onStart} />}
      {aiming.active && <AimingPanel reading={aiming.reading} onDone={aiming.onDone} />}
      {aiming.available && (
        <p className="mb-2.5 text-sm text-text-muted">Ou choisis la direction toi-même :</p>
      )}
      <CompassRose rose={rose} chosen={chosen} onChoose={onChoose} />
      <Hint>Repère : le Soleil se lève vers l'est et se couche vers l'ouest.</Hint>
    </Fieldset>
  );
}
