import { AnswerCard } from "../atoms/AnswerCard";
import { ChoiceButton } from "../atoms/buttons";
import { Eyebrow } from "../atoms/Eyebrow";
import { Sentence } from "../atoms/Sentence";
import { Title } from "../atoms/Title";

interface FeedbackThanksProps {
  readonly hidden: boolean;
  readonly onWriteAnother: () => void;
}

export function FeedbackThanks({ hidden, onWriteAnother }: FeedbackThanksProps) {
  return (
    <AnswerCard hidden={hidden}>
      <Eyebrow flush>Bien reçu</Eyebrow>
      <Title level={2} accent>
        Merci !
      </Title>
      <Sentence>
        Ton message est arrivé chez l'auteur du site. Si tu as laissé ton e-mail, il pourra te
        répondre.
      </Sentence>
      <ChoiceButton onClick={onWriteAnother}>Écrire un autre message</ChoiceButton>
    </AnswerCard>
  );
}
