// Un avis tel que le visiteur l'écrit, et ce qui en part vers l'auteur du site.

import type { FeedbackForm, FeedbackKind } from "./api";
import { WRITE_MESSAGE } from "./texts";

export interface FeedbackDraft {
  readonly kind: FeedbackKind;
  readonly message: string;
  readonly contact: string;
  // Le champ piège : seul un robot le remplit.
  readonly website: string;
}

// Un avis prêt à partir, ou ce qu'il faut encore demander au visiteur.
export type FeedbackCheck = { readonly form: FeedbackForm } | { readonly problem: string };

export function checkFeedback({ kind, message, contact, website }: FeedbackDraft): FeedbackCheck {
  const trimmed = message.trim();
  if (trimmed === "") return { problem: WRITE_MESSAGE };
  return { form: { kind, message: trimmed, contact: contact.trim() || null, website } };
}
