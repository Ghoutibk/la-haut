import { describe, expect, it } from "vitest";

import type { PlanetPosition, VisiblePass } from "./api";
import { answerTo } from "./identification";

const TIANGONG: VisiblePass = {
  kind: "satellite",
  name: "Station spatiale chinoise Tiangong",
  starts_at: "2026-10-05T21:12:00+02:00",
  ends_at: "2026-10-05T21:16:00+02:00",
  duration_s: 240,
  appears_in: { code: "S", label: "sud" },
  vanishes_in: { code: "E", label: "est" },
  max_elevation_deg: 47,
};
const STARLINK_TRAIN: VisiblePass = {
  ...TIANGONG,
  kind: "train",
  name: "Train Starlink (3 satellites)",
  starts_at: "2026-10-05T21:05:00+02:00",
  ends_at: "2026-10-05T21:12:00+02:00",
  appears_in: { code: "W", label: "ouest" },
  vanishes_in: { code: "NE", label: "nord-est" },
  max_elevation_deg: 34,
};

function aPlanet(name: string, label: string, elevation: number): PlanetPosition {
  return { kind: "planet", name, direction: { code: "W", label }, elevation_deg: elevation };
}

const PLANET_EXPLANATION =
  "Une planète ne bouge pas en quelques minutes : elle reste au même endroit parmi les étoiles. Si ta lumière filait dans le ciel, c'était plutôt un satellite ou un avion.";
const SATELLITES_UNCHECKED =
  "Le catalogue des satellites est indisponible pour le moment : seules les planètes ont été vérifiées. Réessaie plus tard pour savoir si c'était un satellite.";

describe("la réponse à « C'était quoi, ça ? »", () => {
  it("donne le passage le plus probable, avec son heure, son chemin et sa hauteur", () => {
    expect(answerTo({ candidates: [TIANGONG], satellites_checked: true })).toEqual({
      eyebrow: "C'était très probablement",
      title: "Station spatiale chinoise Tiangong",
      sentences: [
        "Visible de 21:12 à 21:16, du sud vers l'est.",
        "Au plus haut à 47° au-dessus de l'horizon.",
      ],
    });
  });

  it("explique ce qu'est un train Starlink", () => {
    expect(answerTo({ candidates: [STARLINK_TRAIN], satellites_checked: true }).sentences).toEqual([
      "Visible de 21:05 à 21:12, de l'ouest vers le nord-est.",
      "Au plus haut à 34° au-dessus de l'horizon.",
      "Une file de points brillants qui se suivent : les satellites Starlink d'un même lancement, quelques jours après leur mise en orbite.",
    ]);
  });

  it("donne une planète, ce qu'elle faisait et pourquoi elle ne filait pas", () => {
    const venus = aPlanet("Vénus", "ouest", 12);

    expect(answerTo({ candidates: [venus], satellites_checked: true })).toEqual({
      eyebrow: "C'était très probablement",
      title: "Vénus",
      sentences: ["Vénus brillait vers l'ouest, à 12° au-dessus de l'horizon.", PLANET_EXPLANATION],
    });
  });

  it("propose les autres candidats après le plus probable", () => {
    const answer = answerTo({
      candidates: [TIANGONG, aPlanet("Mars", "sud-est", 18), aPlanet("Saturne", "sud", 30)],
      satellites_checked: true,
    });

    expect(answer.sentences.at(-1)).toBe("Ou peut-être : Mars, Saturne.");
  });

  it("ne donne une planète que peut-être, quand les satellites n'ont pas pu être vérifiés", () => {
    const saturn = aPlanet("Saturne", "sud", 20);

    expect(answerTo({ candidates: [saturn], satellites_checked: false })).toEqual({
      eyebrow: "C'était peut-être",
      title: "Saturne",
      sentences: [
        "Saturne brillait vers le sud, à 20° au-dessus de l'horizon.",
        PLANET_EXPLANATION,
        SATELLITES_UNCHECKED,
      ],
    });
  });

  it("dit que ce n'était ni un satellite ni une planète", () => {
    expect(answerTo({ candidates: [], satellites_checked: true })).toEqual({
      eyebrow: "Rien de connu",
      title: "Ni satellite ni planète",
      sentences: [
        "Aucun satellite suivi ni aucune planète brillante n'était dans cette direction à ce moment. C'était peut-être un avion ou une étoile.",
      ],
    });
  });

  it("dit seulement que ce n'était pas une planète, quand les satellites n'ont pas pu être vérifiés", () => {
    expect(answerTo({ candidates: [], satellites_checked: false })).toEqual({
      eyebrow: "Rien de connu",
      title: "Pas une planète",
      sentences: [
        "Aucune planète brillante n'était dans cette direction à ce moment.",
        SATELLITES_UNCHECKED,
      ],
    });
  });
});
