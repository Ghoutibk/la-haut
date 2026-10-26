import { CloseButton } from "../atoms/buttons";
import { Eyebrow } from "../atoms/Eyebrow";

interface SheetHeaderProps {
  readonly eyebrow: string;
  readonly onClose: () => void;
}

export function SheetHeader({ eyebrow, onClose }: SheetHeaderProps) {
  return (
    <div className="flex items-center justify-between">
      <Eyebrow flush>{eyebrow}</Eyebrow>
      <CloseButton onClick={onClose} />
    </div>
  );
}
