import { describe, expect, it } from "vitest";

import { type SightingReport, checkSighting } from "./sighting";

const NOW = new Date("2026-10-05T21:30:00+02:00");
const A_REPORT: SightingReport = { moment: "now", earlier: "", direction: "NE" };

describe("le signalement d'une lumière", () => {
  it("situe à cet instant une lumière vue à l'instant", () => {
    expect(checkSighting(A_REPORT, NOW)).toEqual({ sighting: { at: NOW, direction: "NE" } });
  });

  it("compte « Il y a 15 min » à partir du moment où le visiteur envoie", () => {
    const report: SightingReport = { ...A_REPORT, moment: "fifteen-minutes-ago" };

    expect(checkSighting(report, NOW)).toEqual({
      sighting: { at: new Date("2026-10-05T21:15:00+02:00"), direction: "NE" },
    });
  });

  it("lit l'heure donnée « Plus tôt » à l'heure du visiteur", () => {
    const report: SightingReport = { ...A_REPORT, moment: "earlier", earlier: "2026-10-05T19:05" };

    expect(checkSighting(report, NOW)).toEqual({
      sighting: { at: new Date("2026-10-05T17:05:00Z"), direction: "NE" },
    });
  });

  it("demande d'abord la direction", () => {
    const report: SightingReport = { moment: "earlier", earlier: "", direction: null };

    expect(checkSighting(report, NOW)).toEqual({ problem: "Choisis la direction où tu l'as vue." });
  });

  it("demande ensuite l'heure, quand la lumière a été vue plus tôt", () => {
    const report: SightingReport = { ...A_REPORT, moment: "earlier", earlier: "" };

    expect(checkSighting(report, NOW)).toEqual({
      problem: "Indique l'heure à laquelle tu l'as vue.",
    });
  });
});
