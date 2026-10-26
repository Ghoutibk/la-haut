import { ChoiceButton } from "../atoms/buttons";
import { ObserverMarker } from "../atoms/ObserverMarker";
import type { CompassPoint, OBSERVER, RoseChoice } from "../../lib/compass";

interface CompassRoseProps {
  // La rose ligne par ligne, le nord en haut et le visiteur au milieu.
  readonly rose: readonly (readonly (RoseChoice | typeof OBSERVER)[])[];
  readonly chosen: CompassPoint | null;
  readonly onChoose: (point: CompassPoint) => void;
}

export function CompassRose({ rose, chosen, onChoose }: CompassRoseProps) {
  return (
    <div className="grid grid-cols-3 gap-2">
      {rose.flat().map((cell) =>
        typeof cell === "string" ? (
          <ObserverMarker key={cell} />
        ) : (
          <ChoiceButton
            key={cell.point}
            shape="rose"
            label={cell.name}
            pressed={cell.point === chosen}
            onClick={() => {
              onChoose(cell.point);
            }}
          >
            {cell.abbreviation}
          </ChoiceButton>
        ),
      )}
    </div>
  );
}
