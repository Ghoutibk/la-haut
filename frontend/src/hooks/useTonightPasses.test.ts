import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { Observer } from "../lib/observer";
import { useTonightPasses } from "./useTonightPasses";

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
  const fetch = vi.fn(() => Promise.resolve(new Response(JSON.stringify(body), { status })));
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

describe("les passages de ce soir, vus par la page", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("attendent la position de l'observateur avant d'être cherchés", () => {
    const fetch = theApiAnswers(200, { passes: [] });

    const { result } = renderHook(() => useTonightPasses(null));

    expect(result.current).toEqual({ status: "Recherche des passages…", passes: [] });
    expect(fetch).not.toHaveBeenCalled();
  });

  it("sont cherchés pour les 12 prochaines heures au-dessus de l'observateur", async () => {
    const fetch = theApiAnswers(200, { passes: [A_PASS] });

    const { result } = renderHook(() => useTonightPasses(LYON));

    await waitFor(() => {
      expect(result.current).toEqual({
        status:
          "Les satellites célèbres et les trains Starlink visibles à l'œil nu dans les 12 prochaines heures.",
        passes: [A_PASS],
      });
    });
    expect(fetch).toHaveBeenCalledWith("/api/passes?latitude=45.76&longitude=4.84&hours=12");
  });

  it("laissent place à la raison pour laquelle la page ne peut pas les annoncer", async () => {
    const detail = "Le catalogue des satellites est indisponible pour le moment, réessaie plus tard.";
    theApiAnswers(503, { detail });

    const { result } = renderHook(() => useTonightPasses(LYON));

    await waitFor(() => {
      expect(result.current).toEqual({ status: detail, passes: [] });
    });
  });
});
