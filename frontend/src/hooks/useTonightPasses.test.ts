import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { A_PASS, LYON, theApiAnswers } from "../testing/doubles";
import { useTonightPasses } from "./useTonightPasses";

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
