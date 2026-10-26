import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { A_PASS, LYON, theApiAnswers, theApiTakesItsTime } from "../testing/doubles";
import { useSightingReport } from "./useSightingReport";

const NOW = new Date("2026-10-05T21:30:00+02:00");
const AN_IDENTIFICATION = { candidates: [A_PASS], satellites_checked: true };

function reporting() {
  return renderHook(() => useSightingReport(LYON));
}

describe("le signalement d'une lumière, vu par la page", () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(NOW);
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("commence à l'instant, sans direction, sans alerte ni réponse", () => {
    const { result } = reporting();

    expect(result.current).toMatchObject({
      moment: "now",
      earlier: "",
      direction: null,
      alert: "",
      busy: false,
      answer: null,
    });
  });

  it("retient le moment, l'heure donnée plus tôt et la direction choisis", () => {
    const { result } = reporting();

    act(() => {
      result.current.chooseMoment("earlier");
      result.current.giveEarlier("2026-10-05T19:05");
      result.current.choosePoint("W");
    });

    expect(result.current).toMatchObject({
      moment: "earlier",
      earlier: "2026-10-05T19:05",
      direction: "W",
    });
  });

  it("alerte sans rien chercher tant que le signalement est incomplet", async () => {
    const fetch = theApiAnswers(200, AN_IDENTIFICATION);
    const { result } = reporting();

    await act(() => result.current.submit());

    expect(result.current.alert).toBe("Choisis la direction où tu l'as vue.");
    expect(result.current.busy).toBe(false);
    expect(fetch).not.toHaveBeenCalled();
  });

  it("efface l'alerte quand le visiteur choisit une direction", async () => {
    const { result } = reporting();
    await act(() => result.current.submit());

    act(() => {
      result.current.choosePoint("N");
    });

    expect(result.current.alert).toBe("");
  });

  it("montre puis efface ce qui empêche de viser", () => {
    const { result } = reporting();

    act(() => {
      result.current.warn("Sans accès à la boussole, choisis la direction toi-même.");
    });
    expect(result.current.alert).toBe("Sans accès à la boussole, choisis la direction toi-même.");

    act(() => {
      result.current.dismissAlert();
    });
    expect(result.current.alert).toBe("");
  });

  it("cherche ce qui était dans la direction au-dessus de l'observateur, puis répond", async () => {
    const fetch = theApiAnswers(200, AN_IDENTIFICATION);
    const { result } = reporting();
    act(() => {
      result.current.chooseMoment("fifteen-minutes-ago");
      result.current.choosePoint("SE");
    });

    await act(() => result.current.submit());

    expect(fetch).toHaveBeenCalledWith(
      "/api/identification?latitude=45.76&longitude=4.84&at=2026-10-05T19%3A15%3A00.000Z&direction=SE",
    );
    expect(result.current.answer).toEqual({
      eyebrow: "C'était très probablement",
      title: "Station spatiale chinoise Tiangong",
      sentences: [
        "Visible de 21:42 à 21:46, du sud vers l'est.",
        "Au plus haut à 17° au-dessus de l'horizon.",
      ],
    });
  });

  it("patiente pendant la recherche, l'alerte précédente effacée", async () => {
    const answer = theApiTakesItsTime();
    const { result } = reporting();
    await act(() => result.current.submit());
    act(() => {
      result.current.choosePoint("E");
      result.current.warn("La boussole de ton téléphone ne répond pas : choisis la direction toi-même.");
    });

    let searching: Promise<void> = Promise.resolve();
    act(() => {
      searching = result.current.submit();
    });
    expect(result.current).toMatchObject({ busy: true, alert: "" });

    await act(async () => {
      answer(200, AN_IDENTIFICATION);
      await searching;
    });
    expect(result.current.busy).toBe(false);
  });

  it("dit pourquoi Là-haut n'a pas pu chercher, et garde la réponse précédente", async () => {
    theApiAnswers(200, AN_IDENTIFICATION);
    const { result } = reporting();
    act(() => {
      result.current.choosePoint("E");
    });
    await act(() => result.current.submit());
    const detail = "Le catalogue des satellites est indisponible pour le moment, réessaie plus tard.";
    theApiAnswers(503, { detail });

    await act(() => result.current.submit());

    await waitFor(() => {
      expect(result.current.alert).toBe(detail);
    });
    expect(result.current.answer?.title).toBe("Station spatiale chinoise Tiangong");
    expect(result.current.busy).toBe(false);
  });
});
