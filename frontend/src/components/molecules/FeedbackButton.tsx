import { ChipButton } from "../atoms/Chip";
import { SpeechBubbleIcon } from "../atoms/icons";

export function FeedbackButton({ onClick }: { readonly onClick: () => void }) {
  return (
    <ChipButton onClick={onClick} opensDialog>
      <SpeechBubbleIcon />
      Avis
    </ChipButton>
  );
}
