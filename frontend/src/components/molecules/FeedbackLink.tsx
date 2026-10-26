import { Hint } from "../atoms/Hint";
import { LinkButton } from "../atoms/buttons";

// Sous une réponse : le visiteur peut dire qu'elle n'était pas la bonne.
export function FeedbackLink({ onClick }: { readonly onClick: () => void }) {
  return (
    <Hint>
      <LinkButton onClick={onClick}>Ce n'était pas ça ? Dis-le-nous</LinkButton>
    </Hint>
  );
}
