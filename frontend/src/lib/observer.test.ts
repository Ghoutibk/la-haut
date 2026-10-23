import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { PARIS, type PositionSource, locateObserver } from "./observer";

type PositionRequest = Parameters<PositionSource["getCurrentPosition"]>;

// Un navigateur qui répond à la demande de position comme le dit `answer`.
function aPositionSource(answer: (request: PositionRequest) => void) {
  const getCurrentPosition = vi.fn((...request: PositionRequest) => {
    answer(request);
  });
  return { getCurrentPosition };
}

describe("la position de l'observateur", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("arrondit au centième la position que le visiteur accepte de donner", async () => {
    const lyon = aPositionSource(([found]) => {
      found({ coords: { latitude: 45.764043, longitude: 4.835659 } });
    });

    await expect(locateObserver(lyon)).resolves.toEqual({
      latitude: 45.76,
      longitude: 4.84,
      label: "Ta position",
    });
  });

  it("se replie sur Paris quand le visiteur refuse de donner sa position", async () => {
    const refused = aPositionSource(([, failed]) => {
      failed();
    });

    await expect(locateObserver(refused)).resolves.toEqual(PARIS);
  });

  it("se replie sur Paris quand le navigateur ne sait pas localiser", async () => {
    await expect(locateObserver(undefined)).resolves.toEqual(PARIS);
  });

  it("n'attend pas plus de 6 secondes une réponse à la demande de position", async () => {
    const unanswered = aPositionSource(() => undefined);
    const located = vi.fn();

    void locateObserver(unanswered).then(located);
    await vi.advanceTimersByTimeAsync(5999);
    expect(located).not.toHaveBeenCalled();
    await vi.advanceTimersByTimeAsync(1);

    expect(located).toHaveBeenCalledWith(PARIS);
  });

  it("accepte une position de moins de 10 minutes, trouvée en 8 secondes au plus", () => {
    const source = aPositionSource(() => undefined);

    void locateObserver(source);

    expect(source.getCurrentPosition.mock.calls[0]?.[2]).toEqual({
      maximumAge: 600_000,
      timeout: 8000,
    });
  });

  it("place Paris à ses coordonnées exactes, sans arrondi", () => {
    expect(PARIS).toEqual({ latitude: 48.8566, longitude: 2.3522, label: "Paris" });
  });
});
