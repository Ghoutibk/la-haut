import { describe, expect, it } from "vitest";

import type { VisiblePass } from "./api";
import { describePass, tonightStatus } from "./tonight";

const MONDAY_EVENING = new Date("2026-10-05T21:30:00+02:00");
const TIANGONG: VisiblePass = {
  kind: "satellite",
  name: "Station spatiale chinoise Tiangong",
  starts_at: "2026-10-05T21:42:00+02:00",
  ends_at: "2026-10-05T21:46:00+02:00",
  duration_s: 240,
  appears_in: { code: "S", label: "sud" },
  vanishes_in: { code: "E", label: "est" },
  max_elevation_deg: 17,
};
const STARLINK_TRAIN: VisiblePass = {
  kind: "train",
  name: "Train Starlink (3 satellites)",
  starts_at: "2026-10-06T05:49:00+02:00",
  ends_at: "2026-10-06T05:56:00+02:00",
  duration_s: 420,
  appears_in: { code: "W", label: "ouest" },
  vanishes_in: { code: "NE", label: "nord-est" },
  max_elevation_deg: 34,
};

describe("la vue « Ce soir »", () => {
  it("annonce les passages qu'elle a trouvés, ou dit quand regarder s'il n'y en a pas", () => {
    expect(tonightStatus([TIANGONG])).toBe(
      "Les satellites célèbres et les trains Starlink visibles à l'œil nu dans les 12 prochaines heures.",
    );
    expect(tonightStatus([])).toBe(
      "Aucun passage visible dans les 12 prochaines heures. Les satellites se voient surtout peu après le coucher du soleil et avant l'aube.",
    );
  });

  it("décrit un passage de ce soir par son heure, son nom, son chemin et sa hauteur", () => {
    expect(describePass(TIANGONG, MONDAY_EVENING)).toEqual({
      time: "21:42",
      day: null,
      name: "Station spatiale chinoise Tiangong",
      path: "sud → est · 4 min",
      peak: "Au plus haut à 17° au-dessus de l'horizon",
      explanation: null,
    });
  });

  it("donne le jour d'un passage qui n'est pas aujourd'hui, et explique un train Starlink", () => {
    expect(describePass(STARLINK_TRAIN, MONDAY_EVENING)).toMatchObject({
      time: "05:49",
      day: "mardi 6 octobre",
      path: "ouest → nord-est · 7 min",
      explanation:
        "Une file de points brillants qui se suivent : les satellites Starlink d'un même lancement, quelques jours après leur mise en orbite.",
    });
  });

  it("compte la durée d'un passage à la minute, une minute au moins", () => {
    const brief = { ...TIANGONG, duration_s: 20 };

    expect(describePass(brief, MONDAY_EVENING).path).toBe("sud → est · 1 min");
  });
});
