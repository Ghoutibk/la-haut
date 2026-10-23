import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { type AimingCallbacks, useAiming } from "./useAiming";

// jsdom connaît l'événement d'orientation ; un téléphone sans boussole, lui, ne le connaît pas.
const ORIENTATION_EVENT = Object.getOwnPropertyDescriptor(window, "DeviceOrientationEvent");

function aScreen(pointer: "coarse" | "fine") {
  vi.stubGlobal("matchMedia", (query: string) => ({ matches: query === `(pointer: ${pointer})` }));
}

function withoutCompass() {
  Reflect.deleteProperty(window, "DeviceOrientationEvent");
}

// Chrome sur Android annonce l'orientation absolue par son propre événement.
function anAndroidPhone() {
  aScreen("coarse");
  vi.stubGlobal("ondeviceorientationabsolute", null);
}

function theOrientationIs(type: string, init: DeviceOrientationEventInit) {
  act(() => {
    window.dispatchEvent(new DeviceOrientationEvent(type, init));
  });
}

function aimingWith(callbacks: Partial<AimingCallbacks> = {}) {
  return renderHook(() => useAiming({ onPoint: vi.fn(), ...callbacks }));
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

  it("suit l'orientation absolue d'Android, de « Lecture de la boussole… » jusqu'à l'arrêt", () => {
    anAndroidPhone();
    const onPoint = vi.fn();
    const { result } = aimingWith({ onPoint });
    expect(result.current.active).toBe(false);

    act(() => {
      result.current.start();
    });
    expect(result.current).toMatchObject({ active: true, reading: "Lecture de la boussole…" });
    theOrientationIs("deviceorientationabsolute", { alpha: 313, absolute: true });
    expect(onPoint).toHaveBeenLastCalledWith("NE");
    expect(result.current.reading).toBe("Tu vises le nord-est");

    act(() => {
      result.current.stop();
    });
    theOrientationIs("deviceorientationabsolute", { alpha: 160, absolute: true });
    expect(result.current.active).toBe(false);
    expect(onPoint).toHaveBeenCalledTimes(1);
  });

  it("écoute l'orientation ordinaire quand l'orientation absolue n'a pas son événement", () => {
    aScreen("coarse");
    const onPoint = vi.fn();
    const { result } = aimingWith({ onPoint });

    act(() => {
      result.current.start();
    });
    theOrientationIs("deviceorientation", { alpha: 10, absolute: false });
    theOrientationIs("deviceorientation", { alpha: 160, absolute: true });

    expect(onPoint.mock.calls).toEqual([["S"]]);
  });

  it("repart de « Lecture de la boussole… » à chaque visée", () => {
    anAndroidPhone();
    const { result } = aimingWith();
    act(() => {
      result.current.start();
    });
    theOrientationIs("deviceorientationabsolute", { alpha: 313, absolute: true });
    act(() => {
      result.current.stop();
    });

    act(() => {
      result.current.start();
    });

    expect(result.current.reading).toBe("Lecture de la boussole…");
  });
});
