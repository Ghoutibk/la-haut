import { IdentificationAnswer } from "../organisms/IdentificationAnswer";
import { SightingForm, type SightingFormProps } from "../organisms/SightingForm";
import { ViewSection } from "../organisms/ViewSection";
import type { Answer } from "../../lib/identification";

interface SightingViewProps {
  readonly hidden: boolean;
  readonly form: SightingFormProps;
  readonly answer: Answer | null;
  // Le visiteur dit que la réponse n'était pas la bonne.
  readonly onFeedback: () => void;
}

export function SightingView({ hidden, form, answer, onFeedback }: SightingViewProps) {
  return (
    <ViewSection
      eyebrow="C'était quoi, ça ?"
      title="Tu as vu une lumière bouger dans le ciel ?"
      hidden={hidden}
    >
      <SightingForm {...form} />
      <IdentificationAnswer answer={answer} onFeedback={onFeedback} />
    </ViewSection>
  );
}
