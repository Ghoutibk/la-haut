import { useEffect, useRef } from "react";

import { AnswerCard } from "../atoms/AnswerCard";
import { Eyebrow } from "../atoms/Eyebrow";
import { Sentence } from "../atoms/Sentence";
import { Title } from "../atoms/Title";
import { FeedbackLink } from "../molecules/FeedbackLink";
import type { Answer } from "../../lib/identification";

interface IdentificationAnswerProps {
  // Rien tant que le visiteur n'a pas demandé.
  readonly answer: Answer | null;
  readonly onFeedback: () => void;
}

export function IdentificationAnswer({ answer, onFeedback }: IdentificationAnswerProps) {
  const card = useRef<HTMLDivElement>(null);

  // Sur un téléphone, la réponse arrive sous le bouton : la page défile juste assez pour la montrer.
  useEffect(() => {
    if (answer !== null) card.current?.scrollIntoView({ block: "nearest" });
  }, [answer]);

  return (
    <AnswerCard ref={card}>
      {answer !== null && (
        <>
          <Eyebrow flush>{answer.eyebrow}</Eyebrow>
          <Title level={2} accent>
            {answer.title}
          </Title>
          {answer.sentences.map((sentence) => (
            <Sentence key={sentence}>{sentence}</Sentence>
          ))}
          <FeedbackLink onClick={onFeedback} />
        </>
      )}
    </AnswerCard>
  );
}
