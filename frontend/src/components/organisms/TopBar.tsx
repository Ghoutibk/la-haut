import { Brand } from "../molecules/Brand";
import { FeedbackButton } from "../molecules/FeedbackButton";
import { PlaceChip } from "../molecules/PlaceChip";

export interface TopBarProps {
  readonly place: string;
  readonly onFeedback: () => void;
}

export function TopBar({ place, onFeedback }: TopBarProps) {
  return (
    <header className="mb-7 flex items-center justify-between gap-3">
      <Brand />
      <div className="flex items-center gap-2">
        <PlaceChip place={place} />
        <FeedbackButton onClick={onFeedback} />
      </div>
    </header>
  );
}
