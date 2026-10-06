import assert from "node:assert/strict";
import { test } from "node:test";

import {
  COMPASS_POINTS,
  FRENCH_NAMES,
  compassPointOf,
  headingFrom,
} from "../../src/la_haut/interface/http/static/compass.js";

test("un cap tombe dans le secteur de son point cardinal, découpé comme dans le domaine", () => {
  const headings = [0, 22.4, 22.5, 90, 200, 337.4, 337.5, 359.9];

  assert.deepEqual(headings.map(compassPointOf), ["N", "N", "NE", "E", "S", "NW", "N", "N"]);
});

test("sur iPhone, le cap vient directement de la boussole", () => {
  assert.equal(headingFrom({ webkitCompassHeading: 47, alpha: 120, absolute: false }), 47);
});

test("une boussole d'iPhone pas encore étalonnée ne donne aucun cap", () => {
  assert.equal(headingFrom({ webkitCompassHeading: -1, alpha: 120, absolute: false }), null);
});

test("sur Android, l'orientation absolue compte ses degrés dans l'autre sens", () => {
  assert.equal(headingFrom({ absolute: true, alpha: 313 }), 47);
});

test("plein nord sur Android donne 0 degré, pas 360", () => {
  assert.equal(headingFrom({ absolute: true, alpha: 0 }), 0);
});

test("une orientation qui ne sait pas où est le nord ne donne aucun cap", () => {
  assert.equal(headingFrom({ absolute: false, alpha: 10 }), null);
  assert.equal(headingFrom({ absolute: true, alpha: null }), null);
});

test("chaque point cardinal a son nom en français", () => {
  assert.deepEqual(Object.keys(FRENCH_NAMES), COMPASS_POINTS);
  assert.equal(FRENCH_NAMES.NE, "nord-est");
});
