import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { theApiAnswers, theApiTakesItsTime } from "../testing/doubles";
import { useFeedback } from "./useFeedback";

const AN_IDEA = "Ajouter les passages de la Lune";

function writingFeedback(initiallyOpen = false) {
  return renderHook(() => useFeedback(initiallyOpen));
}

function aSentIdea() {
  const view = writingFeedback(true);
  act(() => {
    view.result.current.revise({ kind: "idea", message: AN_IDEA, contact: "claire@example.org" });
  });
  return view;
}

describe("la fenêtre d'avis, vue par la page", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("s'ouvre au chargement seulement quand on le lui demande", () => {
    expect(writingFeedback().result.current.isOpen).toBe(false);
    expect(writingFeedback(true).result.current.isOpen).toBe(true);
  });

  it("commence par un problème, sans message ni e-mail", () => {
    expect(writingFeedback().result.current).toMatchObject({
      draft: { kind: "problem", message: "", contact: "", website: "" },
      alert: "",
      busy: false,
      thanked: false,
    });
  });

  it("s'ouvre et se ferme", () => {
    const { result } = writingFeedback();

    act(() => {
      result.current.open();
    });
    expect(result.current.isOpen).toBe(true);

    act(() => {
      result.current.close();
    });
    expect(result.current.isOpen).toBe(false);
  });

  it("n'envoie pas un message vide, et le dit", async () => {
    const fetch = theApiAnswers(201, { status: "sent" });
    const { result } = writingFeedback(true);

    await act(() => result.current.send());

    expect(result.current.alert).toBe("Écris ton message avant de l'envoyer.");
    expect(result.current.busy).toBe(false);
    expect(fetch).not.toHaveBeenCalled();
  });

  it("se rouvre sur le brouillon, sans l'ancienne alerte", async () => {
    const { result } = writingFeedback(true);
    act(() => {
      result.current.revise({ contact: "claire@example.org" });
    });
    await act(() => result.current.send());

    act(() => {
      result.current.close();
      result.current.open();
    });

    expect(result.current.alert).toBe("");
    expect(result.current.draft.contact).toBe("claire@example.org");
  });

  it("envoie l'avis vérifié, puis remercie sur un formulaire vidé qui garde sa nature", async () => {
    const fetch = theApiAnswers(201, { status: "sent" });
    const { result } = aSentIdea();

    await act(() => result.current.send());

    expect(fetch).toHaveBeenCalledWith(
      "/api/feedback",
      expect.objectContaining({
        body: JSON.stringify({
          kind: "idea",
          message: AN_IDEA,
          contact: "claire@example.org",
          website: "",
        }),
      }),
    );
    expect(result.current).toMatchObject({
      draft: { kind: "idea", message: "", contact: "", website: "" },
      thanked: true,
      busy: false,
    });
  });

  it("patiente pendant l'envoi, l'alerte précédente effacée", async () => {
    const answer = theApiTakesItsTime();
    const { result } = writingFeedback(true);
    await act(() => result.current.send());
    act(() => {
      result.current.revise({ message: AN_IDEA });
    });

    let sending: Promise<void> = Promise.resolve();
    act(() => {
      sending = result.current.send();
    });
    expect(result.current).toMatchObject({ busy: true, alert: "" });

    await act(async () => {
      answer(201, { status: "sent" });
      await sending;
    });
    expect(result.current.busy).toBe(false);
  });

  it("dit pourquoi l'avis n'est pas parti, et garde le brouillon", async () => {
    theApiAnswers(422, { detail: "Cette adresse e-mail ne semble pas valide." });
    const { result } = aSentIdea();

    await act(() => result.current.send());

    expect(result.current).toMatchObject({
      alert: "Cette adresse e-mail ne semble pas valide.",
      thanked: false,
      busy: false,
      draft: { message: AN_IDEA },
    });
  });

  it("revient au formulaire pour écrire un autre message, ou quand elle se rouvre", async () => {
    theApiAnswers(201, { status: "sent" });
    const { result } = aSentIdea();
    await act(() => result.current.send());

    act(() => {
      result.current.writeAnother();
    });
    expect(result.current.thanked).toBe(false);

    act(() => {
      result.current.revise({ message: AN_IDEA });
    });
    await act(() => result.current.send());
    act(() => {
      result.current.close();
      result.current.open();
    });
    expect(result.current.thanked).toBe(false);
  });
});
