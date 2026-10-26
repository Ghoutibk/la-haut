import { renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { PARIS, type PositionSource } from "../lib/observer";
import { useObserverLocation } from "./useObserverLocation";

function theBrowserLocates(source: PositionSource) {
  Object.defineProperty(navigator, "geolocation", { value: source, configurable: true });
}

describe("la position de l'observateur, vue par la page", () => {
  afterEach(() => {
    Reflect.deleteProperty(navigator, "geolocation");
  });

  it("reste inconnue tant que le navigateur n'a pas répondu", () => {
    theBrowserLocates({ getCurrentPosition: () => undefined });

    const { result } = renderHook(() => useObserverLocation());

    expect(result.current).toBeNull();
  });

  it("devient celle que le visiteur accepte de donner", async () => {
    theBrowserLocates({
      getCurrentPosition: (found) => {
        found({ coords: { latitude: 45.764043, longitude: 4.835659 } });
      },
    });

    const { result } = renderHook(() => useObserverLocation());

    await waitFor(() => {
      expect(result.current).toEqual({ latitude: 45.76, longitude: 4.84, label: "Ta position" });
    });
  });

  it("devient Paris quand le navigateur ne sait pas localiser", async () => {
    const { result } = renderHook(() => useObserverLocation());

    await waitFor(() => {
      expect(result.current).toEqual(PARIS);
    });
  });
});
