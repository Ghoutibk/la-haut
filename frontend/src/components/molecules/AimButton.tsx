import { OutlineButton } from "../atoms/buttons";
import { CompassIcon } from "../atoms/icons";

export function AimButton({ onClick }: { readonly onClick: () => void }) {
  return (
    <OutlineButton onClick={onClick}>
      <CompassIcon />
      Viser avec mon téléphone
    </OutlineButton>
  );
}
