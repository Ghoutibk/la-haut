import { describe, expect, it } from "vitest";

import { isOutside } from "./dialog";

const SHEET = { left: 0, right: 390, top: 300, bottom: 844 };

describe("un toucher autour de la fenêtre", () => {
  it("tombe hors de la fenêtre au-dessus, en dessous ou sur les côtés", () => {
    const touches = [
      { x: 195, y: 150 },
      { x: 195, y: 900 },
      { x: -1, y: 500 },
      { x: 391, y: 500 },
    ];

    expect(touches.map((touch) => isOutside(SHEET, touch))).toEqual([true, true, true, true]);
  });

  it("tombe dans la fenêtre jusqu'à son bord", () => {
    const touches = [
      { x: 195, y: 304 },
      { x: 0, y: 300 },
      { x: 390, y: 844 },
    ];

    expect(touches.map((touch) => isOutside(SHEET, touch))).toEqual([false, false, false]);
  });
});
