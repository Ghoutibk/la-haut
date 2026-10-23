import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { useHashView } from "./useHashView";

describe("la vue ouverte par l'adresse", () => {
  afterEach(() => {
    window.history.replaceState(null, "", "/");
  });

  it("est celle de l'ancre de la page au chargement", () => {
    window.history.replaceState(null, "", "/#cetait-quoi");

    const { result } = renderHook(() => useHashView());

    expect(result.current).toBe("sighting");
  });

  it("suit l'ancre quand elle change", async () => {
    const { result } = renderHook(() => useHashView());
    expect(result.current).toBe("tonight");

    window.location.hash = "#cetait-quoi";

    await waitFor(() => {
      expect(result.current).toBe("sighting");
    });
  });
});
