// Les doublures et les données partagées par les tests de la page : une seule source pour chacune.

import { vi } from "vitest";

import type { VisiblePass } from "../lib/api";
import type { Observer } from "../lib/observer";

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
