import { useState } from "react";

import { failureMessage, sendFeedback } from "../lib/api";
import { type FeedbackDraft, checkFeedback } from "../lib/feedback";

const A_BLANK_DRAFT: FeedbackDraft = { kind: "problem", message: "", contact: "", website: "" };

export interface FeedbackWindow {
  readonly isOpen: boolean;
  readonly open: () => void;
  readonly close: () => void;
  readonly draft: FeedbackDraft;
  readonly revise: (changes: Partial<FeedbackDraft>) => void;
  // Ce que la fenêtre signale au visiteur : un message vide ou un refus de Là-haut ; vide sinon.
  readonly alert: string;
  readonly busy: boolean;
  // Le message est arrivé : la fenêtre remercie au lieu de montrer le formulaire.
  readonly thanked: boolean;
  readonly send: () => Promise<void>;
  readonly writeAnother: () => void;
}

// La fenêtre d'avis : ouverte au chargement si on le lui demande, puis par le visiteur.
export function useFeedback(initiallyOpen: boolean): FeedbackWindow {
  const [isOpen, setIsOpen] = useState(initiallyOpen);
  const [draft, setDraft] = useState(A_BLANK_DRAFT);
  const [alert, setAlert] = useState("");
  const [busy, setBusy] = useState(false);
  const [thanked, setThanked] = useState(false);

  // Elle s'ouvre toujours sur le formulaire, avec le brouillon et sans l'ancienne alerte.
  function open() {
    setThanked(false);
    setAlert("");
    setIsOpen(true);
  }

  async function send() {
    const check = checkFeedback(draft);
    if ("problem" in check) {
      setAlert(check.problem);
      return;
    }
    setAlert("");
    setBusy(true);
    try {
      await sendFeedback(check.form);
      setDraft({ ...A_BLANK_DRAFT, kind: draft.kind });
      setThanked(true);
    } catch (error) {
      setAlert(failureMessage(error));
    } finally {
      setBusy(false);
    }
  }

  return {
    isOpen,
    open,
    close: () => {
      setIsOpen(false);
    },
    draft,
    revise: (changes) => {
      setDraft((current) => ({ ...current, ...changes }));
    },
    alert,
    busy,
    thanked,
    send,
    writeAnother: () => {
      setThanked(false);
    },
  };
}
