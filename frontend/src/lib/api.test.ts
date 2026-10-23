import { afterEach, describe, expect, it, vi } from "vitest";

import { failureMessage, identify, searchPasses, sendFeedback } from "./api";
import type { Observer } from "./observer";

const LYON: Observer = { latitude: 45.76, longitude: 4.84, label: "Ta position" };
const A_PASS = {
  kind: "satellite",
  name: "Station spatiale chinoise Tiangong",
  starts_at: "2026-10-05T21:42:00+02:00",
  ends_at: "2026-10-05T21:46:00+02:00",
  duration_s: 240,
  appears_in: { code: "S", label: "sud" },
  vanishes_in: { code: "E", label: "est" },
  max_elevation_deg: 17,
};

function theApiAnswers(status: number, body: unknown) {
  const fetch = vi.fn(() =>
    Promise.resolve(
      new Response(typeof body === "string" ? body : JSON.stringify(body), { status }),
    ),
  );
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

describe("les appels à l'API de Là-haut", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("cherche les passages des prochaines heures au-dessus de l'observateur", async () => {
    const fetch = theApiAnswers(200, { passes: [A_PASS] });

    await expect(searchPasses(LYON, 12)).resolves.toEqual([A_PASS]);
    expect(fetch).toHaveBeenCalledWith("/api/passes?latitude=45.76&longitude=4.84&hours=12");
  });

  it("demande ce qui était dans une direction, à un instant donné en temps universel", async () => {
    const fetch = theApiAnswers(200, { candidates: [A_PASS], satellites_checked: true });
    const sighting = { at: new Date("2026-10-05T21:30:00+02:00"), direction: "NE" } as const;

    await expect(identify(LYON, sighting)).resolves.toEqual({
      candidates: [A_PASS],
      satellites_checked: true,
    });
    expect(fetch).toHaveBeenCalledWith(
      "/api/identification?latitude=45.76&longitude=4.84&at=2026-10-05T19%3A30%3A00.000Z&direction=NE",
    );
  });

  it("donne l'explication de l'API quand elle refuse de chercher", async () => {
    const detail = "Le catalogue des satellites est indisponible pour le moment, réessaie plus tard.";
    theApiAnswers(503, { detail });

    await expect(searchPasses(LYON, 12)).rejects.toThrow(detail);
  });

  it("dit que le ciel est injoignable quand la réponse n'explique rien", async () => {
    theApiAnswers(502, "<html><body><h1>502 Bad Gateway</h1></body></html>");

    await expect(searchPasses(LYON, 12)).rejects.toThrow("Le ciel est injoignable pour le moment.");
  });

  it("envoie un avis en JSON", async () => {
    const fetch = theApiAnswers(201, { status: "sent" });
    const feedback = { kind: "idea", message: "La Lune", contact: null, website: "" } as const;

    await sendFeedback(feedback);

    expect(fetch).toHaveBeenCalledWith("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(feedback),
    });
  });

  it("donne l'explication de l'API quand elle refuse un avis, ou dit qu'il n'a pas pu partir", async () => {
    const feedback = { kind: "problem", message: "Oups", contact: "claire@", website: "" } as const;
    theApiAnswers(422, { detail: "Cette adresse e-mail ne semble pas valide." });
    await expect(sendFeedback(feedback)).rejects.toThrow("Cette adresse e-mail ne semble pas valide.");

    theApiAnswers(502, "<html></html>");
    await expect(sendFeedback(feedback)).rejects.toThrow(
      "Ton message n'a pas pu partir : vérifie-le et réessaie.",
    );
  });

  it("lit le message d'un échec pour l'afficher tel quel", () => {
    expect(failureMessage(new Error("Le ciel est injoignable pour le moment."))).toBe(
      "Le ciel est injoignable pour le moment.",
    );
    expect(failureMessage("coupure")).toBe("coupure");
  });
});
