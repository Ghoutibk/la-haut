// L'appareil du visiteur, simulé dans jsdom : son écran, sa boussole et ce qu'elle annonce.
// vi.unstubAllGlobals() le rend tel qu'il était.

import { act } from "@testing-library/react";
import { vi } from "vitest";

export function aScreen(pointer: "coarse" | "fine") {
  vi.stubGlobal("matchMedia", (query: string) => ({ matches: query === `(pointer: ${pointer})` }));
}

// Chrome sur Android annonce l'orientation absolue par son propre événement.
export function anAndroidPhone() {
  aScreen("coarse");
  vi.stubGlobal("ondeviceorientationabsolute", null);
}

export function theOrientationIs(type: string, init: DeviceOrientationEventInit) {
  act(() => {
    window.dispatchEvent(new DeviceOrientationEvent(type, init));
  });
}
