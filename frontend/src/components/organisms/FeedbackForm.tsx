import { BotTrap } from "../atoms/BotTrap";
import { ErrorText } from "../atoms/ErrorText";
import { Field } from "../atoms/Field";
import { Hint } from "../atoms/Hint";
import { PrimaryButton } from "../atoms/buttons";
import { EmailInput, TextArea } from "../atoms/inputs";
import { ChoiceGroup, type Choice } from "../molecules/ChoiceGroup";
import type { FeedbackKind } from "../../lib/api";
import type { FeedbackDraft } from "../../lib/feedback";

// Les longueurs que l'API accepte : un message de deux mille caractères, une adresse e-mail.
const MESSAGE_MAX_LENGTH = 2000;
const CONTACT_MAX_LENGTH = 254;

const KINDS: readonly Choice<FeedbackKind>[] = [
  { value: "problem", label: "Un problème" },
  { value: "idea", label: "Une idée" },
  { value: "other", label: "Autre chose" },
];

export interface FeedbackFormProps {
  readonly draft: FeedbackDraft;
  readonly onRevise: (changes: Partial<FeedbackDraft>) => void;
  readonly alert: string;
  readonly busy: boolean;
  readonly onSend: () => void;
  readonly hidden: boolean;
}

export function FeedbackForm({ draft, onRevise, alert, busy, onSend, hidden }: FeedbackFormProps) {
  return (
    <form
      noValidate
      hidden={hidden}
      onSubmit={(event) => {
        event.preventDefault();
        onSend();
      }}
    >
      <ChoiceGroup
        legend="C'est plutôt…"
        choices={KINDS}
        chosen={draft.kind}
        onChoose={(kind) => {
          onRevise({ kind });
        }}
      />
      <Field label="Ton message">
        <TextArea
          value={draft.message}
          onChange={(message) => {
            onRevise({ message });
          }}
          maxLength={MESSAGE_MAX_LENGTH}
          placeholder="Par exemple : la boussole ne bouge pas sur mon téléphone."
        />
      </Field>
      <Field label="Ton e-mail, si tu veux une réponse (facultatif)">
        <EmailInput
          value={draft.contact}
          onChange={(contact) => {
            onRevise({ contact });
          }}
          maxLength={CONTACT_MAX_LENGTH}
        />
      </Field>
      <Hint>Ton e-mail ne sert qu'à te répondre. Il n'est jamais affiché sur le site.</Hint>
      <BotTrap
        value={draft.website}
        onChange={(website) => {
          onRevise({ website });
        }}
      />
      <ErrorText>{alert}</ErrorText>
      <PrimaryButton busy={busy}>Envoyer</PrimaryButton>
    </form>
  );
}
