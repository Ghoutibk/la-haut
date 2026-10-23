import { describe, expect, it } from "vitest";

import { VIEW_ANCHORS, opensFeedback, viewOf } from "./route";

describe("l'adresse de la page", () => {
  it("ouvre chaque vue à son ancre", () => {
    expect(viewOf(VIEW_ANCHORS.tonight)).toBe("tonight");
    expect(viewOf(VIEW_ANCHORS.sighting)).toBe("sighting");
    expect(VIEW_ANCHORS).toEqual({ tonight: "#ce-soir", sighting: "#cetait-quoi" });
  });

  it("ouvre « Ce soir » sans ancre ou pour une ancre inconnue", () => {
    expect(["", "#n-importe-quoi", "#avis"].map(viewOf)).toEqual(["tonight", "tonight", "tonight"]);
  });

  it("ouvre la fenêtre d'avis à l'ancienne ancre de l'onglet « Ton avis »", () => {
    expect(["#avis", "#ce-soir", ""].map(opensFeedback)).toEqual([true, false, false]);
  });
});
