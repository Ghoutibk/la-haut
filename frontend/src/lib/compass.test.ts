import { describe, expect, it } from "vitest";

import {
  COMPASS_POINTS,
  COMPASS_ROSE,
  FRENCH_NAMES,
  OBSERVER,
  compassPointOf,
  headingFrom,
} from "./compass";

describe("la boussole du téléphone", () => {
  it("range un cap dans le secteur de son point cardinal, découpé comme dans le domaine", () => {
    const headings = [0, 22.4, 22.5, 90, 200, 337.4, 337.5, 359.9];

    expect(headings.map(compassPointOf)).toEqual(["N", "N", "NE", "E", "S", "NW", "N", "N"]);
  });

  it("lit le cap directement dans la boussole d'un iPhone", () => {
    expect(headingFrom({ webkitCompassHeading: 47, alpha: 120, absolute: false })).toBe(47);
  });

  it("ne donne aucun cap tant que la boussole de l'iPhone n'est pas étalonnée", () => {
    expect(headingFrom({ webkitCompassHeading: -1, alpha: 120, absolute: false })).toBeNull();
  });

  it("compte dans l'autre sens les degrés de l'orientation absolue d'Android", () => {
    expect(headingFrom({ absolute: true, alpha: 313 })).toBe(47);
  });

  it("donne 0 degré, pas 360, pour le plein nord sur Android", () => {
    expect(headingFrom({ absolute: true, alpha: 0 })).toBe(0);
  });

  it("ne donne aucun cap pour une orientation qui ne sait pas où est le nord", () => {
    expect(headingFrom({ absolute: false, alpha: 10 })).toBeNull();
    expect(headingFrom({ absolute: true, alpha: null })).toBeNull();
  });

  it("nomme chaque point cardinal en français", () => {
    expect(Object.keys(FRENCH_NAMES)).toEqual(COMPASS_POINTS);
    expect(FRENCH_NAMES.NE).toBe("nord-est");
  });

  it("dispose la rose des vents autour de l'observateur, le nord en haut", () => {
    const cells = COMPASS_ROSE.map((row) =>
      row.map((cell) => (cell === OBSERVER ? "Toi" : `${cell.abbreviation} (${cell.name})`)),
    );

    expect(cells).toEqual([
      ["NO (Nord-ouest)", "N (Nord)", "NE (Nord-est)"],
      ["O (Ouest)", "Toi", "E (Est)"],
      ["SO (Sud-ouest)", "S (Sud)", "SE (Sud-est)"],
    ]);
  });
});
