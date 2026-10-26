import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { aScreen, anAndroidPhone, theOrientationIs } from "../testing/phone";
import { type AimingCallbacks, useAiming } from "./useAiming";

// jsdom connaît l'événement d'orientation ; un téléphone sans boussole, lui, ne le connaît pas.
const ORIENTATION_EVENT = Object.getOwnPropertyDescriptor(window, "DeviceOrientationEvent");

function withoutCompass() {
  Reflect.deleteProperty(window, "DeviceOrientationEvent");
}

// Safari sur iPhone demande au visiteur l'accès à la boussole, puis donne le cap directement.
function anIphone(answer: () => Promise<string>) {
  aScreen("coarse");
  const requestPermission = vi.fn(answer);
  Object.defineProperty(DeviceOrientationEvent, "requestPermission", {
    value: requestPermission,
    configurable: true,
  });
  return requestPermission;
}

function theIphoneCompassReads(heading: number) {
  const event = new DeviceOrientationEvent("deviceorientation", { alpha: 120, absolute: false });
  Object.defineProperty(event, "webkitCompassHeading", { value: heading });
  act(() => {
    window.dispatchEvent(event);
  });
}

function secondsGoBy(seconds: number) {
  act(() => {
    vi.advanceTimersByTime(seconds * 1000);
  });
}

function aimingWith(callbacks: Partial<AimingCallbacks> = {}) {
  return renderHook(() => useAiming({ onPoint: vi.fn(), onError: vi.fn(), ...callbacks }));
}

describe("viser avec le téléphone", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    if (ORIENTATION_EVENT) Object.defineProperty(window, "DeviceOrientationEvent", ORIENTATION_EVENT);
    Reflect.deleteProperty(DeviceOrientationEvent, "requestPermission");
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

  it("suit l'orientation absolue d'Android, de « Lecture de la boussole… » jusqu'à l'arrêt", async () => {
    anAndroidPhone();
    const onPoint = vi.fn();
    const { result } = aimingWith({ onPoint });
    expect(result.current.active).toBe(false);

    await act(() => result.current.start());
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

  it("écoute l'orientation ordinaire quand l'orientation absolue n'a pas son événement", async () => {
    aScreen("coarse");
    const onPoint = vi.fn();
    const { result } = aimingWith({ onPoint });

    await act(() => result.current.start());
    theOrientationIs("deviceorientation", { alpha: 10, absolute: false });
    theOrientationIs("deviceorientation", { alpha: 160, absolute: true });

    expect(onPoint.mock.calls).toEqual([["S"]]);
  });

  it("repart de « Lecture de la boussole… » à chaque visée", async () => {
    anAndroidPhone();
    const { result } = aimingWith();
    await act(() => result.current.start());
    theOrientationIs("deviceorientationabsolute", { alpha: 313, absolute: true });
    act(() => {
      result.current.stop();
    });

    await act(() => result.current.start());

    expect(result.current.reading).toBe("Lecture de la boussole…");
  });

  it("abandonne au bout de 3 secondes une boussole qui ne sait pas où est le nord", async () => {
    vi.useFakeTimers();
    anAndroidPhone();
    const onError = vi.fn();
    const { result } = aimingWith({ onError });
    await act(() => result.current.start());

    theOrientationIs("deviceorientationabsolute", { alpha: 10, absolute: false });
    secondsGoBy(2.999);
    expect(result.current.active).toBe(true);
    secondsGoBy(0.001);

    expect(result.current.active).toBe(false);
    expect(onError).toHaveBeenCalledWith(
      "La boussole de ton téléphone ne répond pas : choisis la direction toi-même.",
    );
  });

  it("garde une boussole qui a donné un cap, même s'il tarde à changer", async () => {
    vi.useFakeTimers();
    anAndroidPhone();
    const onError = vi.fn();
    const { result } = aimingWith({ onError });
    await act(() => result.current.start());

    theOrientationIs("deviceorientationabsolute", { alpha: 313, absolute: true });
    secondsGoBy(3);

    expect(result.current.active).toBe(true);
    expect(onError).not.toHaveBeenCalled();
  });

  it("ne s'impatiente plus une fois la visée arrêtée", async () => {
    vi.useFakeTimers();
    anAndroidPhone();
    const onError = vi.fn();
    const { result } = aimingWith({ onError });
    await act(() => result.current.start());
    act(() => {
      result.current.stop();
    });

    secondsGoBy(3);

    expect(onError).not.toHaveBeenCalled();
  });

  it("demande l'accès à la boussole de l'iPhone au moment de viser, puis lit son cap", async () => {
    const requestPermission = anIphone(() => Promise.resolve("granted"));
    const onPoint = vi.fn();
    const { result } = aimingWith({ onPoint });
    expect(requestPermission).not.toHaveBeenCalled();

    await act(() => result.current.start());
    theIphoneCompassReads(-1);
    expect(result.current.reading).toBe("Lecture de la boussole…");
    theIphoneCompassReads(135);

    expect(requestPermission).toHaveBeenCalledTimes(1);
    expect(onPoint.mock.calls).toEqual([["SE"]]);
  });

  it.each([
    ["refuse", () => Promise.resolve("denied")],
    ["échoue", () => Promise.reject(new DOMException("refusé", "NotAllowedError"))],
  ])("ne vise pas quand l'accès à la boussole de l'iPhone %s", async (_, answer) => {
    anIphone(answer);
    const onError = vi.fn();
    const { result } = aimingWith({ onError });

    await act(() => result.current.start());

    expect(result.current.active).toBe(false);
    expect(onError).toHaveBeenCalledWith("Sans accès à la boussole, choisis la direction toi-même.");
  });
});
