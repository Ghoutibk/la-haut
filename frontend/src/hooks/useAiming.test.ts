import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useAiming } from "./useAiming";

// jsdom connaît l'événement d'orientation ; un téléphone sans boussole, lui, ne le connaît pas.
const ORIENTATION_EVENT = Object.getOwnPropertyDescriptor(window, "DeviceOrientationEvent");

function aScreen(pointer: "coarse" | "fine") {
  vi.stubGlobal("matchMedia", (query: string) => ({ matches: query === `(pointer: ${pointer})` }));
}

function withoutCompass() {
  Reflect.deleteProperty(window, "DeviceOrientationEvent");
}

function aimingWith() {
  return renderHook(() => useAiming());
}

describe("viser avec le téléphone", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    if (ORIENTATION_EVENT) Object.defineProperty(window, "DeviceOrientationEvent", ORIENTATION_EVENT);
  });

  it("se propose sur un téléphone qui a une boussole", () => {
    aScreen("coarse");

    expect(aimingWith().result.current.available).toBe(true);
  });

  it("ne se propose pas sur un ordinateur", () => {
    aScreen("fine");

    expect(aimingWith().result.current.available).toBe(false);
  });

  it("ne se propose pas sur un téléphone sans boussole", () => {
    aScreen("coarse");
    withoutCompass();

    expect(aimingWith().result.current.available).toBe(false);
  });
});
