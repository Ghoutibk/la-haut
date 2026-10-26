// Les doublures et les données partagées par les tests de la page : une seule source pour chacune.

import { vi } from "vitest";

import type { VisiblePass } from "../lib/api";
import type { Observer } from "../lib/observer";
import type { PassDescription } from "../lib/tonight";

export const LYON: Observer = { latitude: 45.76, longitude: 4.84, label: "Ta position" };

export const A_PASS: VisiblePass = {
  kind: "satellite",
  name: "Station spatiale chinoise Tiangong",
  starts_at: "2026-10-05T21:42:00+02:00",
  ends_at: "2026-10-05T21:46:00+02:00",
  duration_s: 240,
  appears_in: { code: "S", label: "sud" },
  vanishes_in: { code: "E", label: "est" },
  max_elevation_deg: 17,
};

// Le même passage, tel que la vue « Ce soir » le décrit.
export const A_PASS_DESCRIPTION: PassDescription = {
  time: "21:42",
  day: null,
  name: "Station spatiale chinoise Tiangong",
  path: "sud → est · 4 min",
  peak: "Au plus haut à 17° au-dessus de l'horizon",
  explanation: null,
};

// L'API répond toujours ainsi ; un corps textuel est rendu tel quel, comme une page d'erreur.
export function theApiAnswers(status: number, body: unknown) {
  const fetch = vi.fn(() =>
    Promise.resolve(
      new Response(typeof body === "string" ? body : JSON.stringify(body), { status }),
    ),
  );
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

// L'API ne répond que quand le test le décide, par la fonction rendue.
export function theApiTakesItsTime(): (status: number, body: unknown) => void {
  let answer: (response: Response) => void = () => undefined;
  vi.stubGlobal(
    "fetch",
    vi.fn(() => new Promise<Response>((resolve) => (answer = resolve))),
  );
  return (status, body) => {
    answer(new Response(JSON.stringify(body), { status }));
  };
}
