import { Chip } from "../atoms/Chip";
import { PinIcon } from "../atoms/icons";

// D'où le visiteur regarde le ciel : sa position, ou Paris.
export function PlaceChip({ place }: { readonly place: string }) {
  return (
    <Chip>
      <PinIcon />
      <span>{place}</span>
    </Chip>
  );
}
