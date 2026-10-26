import { describe, expect, it } from "vitest";

import { type FeedbackDraft, checkFeedback } from "./feedback";

const A_DRAFT: FeedbackDraft = {
  kind: "problem",
  message: "  La boussole ne bouge pas \n",
  contact: " claire@example.org ",
  website: "",
};

describe("un avis avant l'envoi", () => {
  it("ne part pas sans message, même fait d'espaces", () => {
    expect(checkFeedback({ ...A_DRAFT, message: " \n " })).toEqual({
      problem: "Écris ton message avant de l'envoyer.",
    });
  });

  it("part sans les espaces autour du message et de l'e-mail", () => {
    expect(checkFeedback(A_DRAFT)).toEqual({
      form: {
        kind: "problem",
        message: "La boussole ne bouge pas",
        contact: "claire@example.org",
        website: "",
      },
    });
  });

  it("part sans e-mail quand le visiteur n'en laisse pas", () => {
    expect(checkFeedback({ ...A_DRAFT, kind: "idea", contact: "  " })).toMatchObject({
      form: { kind: "idea", contact: null },
    });
  });

  it("laisse le champ piège tel qu'un robot l'a rempli", () => {
    expect(checkFeedback({ ...A_DRAFT, website: "https://spam.example" })).toMatchObject({
      form: { website: "https://spam.example" },
    });
  });
});
