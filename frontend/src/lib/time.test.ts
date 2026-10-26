import { describe, expect, it } from "vitest";

import { clockTime, dayName, isSameDay, minutesOf } from "./time";

// Les tests tournent à l'heure de Paris (TZ=Europe/Paris, voir vite.config.ts).
describe("l'heure et le jour, à l'heure du visiteur", () => {
  it("lit l'heure en heures et minutes", () => {
    expect(clockTime(new Date("2026-10-05T19:42:00Z"))).toBe("21:42");
    expect(clockTime(new Date("2026-10-06T03:05:59Z"))).toBe("05:05");
  });

  it("nomme le jour, sans l'année", () => {
    expect(dayName(new Date("2026-10-06T03:49:00Z"))).toBe("mardi 6 octobre");
  });

  it("compare les jours là où vit le visiteur, pas en temps universel", () => {
    const justAfterMidnightInParis = new Date("2026-10-05T22:30:00Z");

    expect(isSameDay(new Date("2026-10-06T03:49:00Z"), justAfterMidnightInParis)).toBe(true);
    expect(isSameDay(new Date("2026-10-05T21:59:00Z"), justAfterMidnightInParis)).toBe(false);
  });

  it("arrondit une durée à la minute, une minute au moins", () => {
    expect([20, 89, 90, 240, 280].map(minutesOf)).toEqual([1, 1, 2, 4, 5]);
  });
});
