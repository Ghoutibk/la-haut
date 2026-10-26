import { act, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { A_PASS, LYON, theApiAnswers } from "../../testing/doubles";
import { anAndroidPhone, theOrientationIs } from "../../testing/phone";
import { SightingPage } from "./SightingPage";

const AIM = "Viser avec mon téléphone";
const NORTH_EAST = { alpha: 313, absolute: true };

function aSightingPage(onFeedback = vi.fn()) {
  render(<SightingPage observer={LYON} hidden={false} onFeedback={onFeedback} />);
  return screen.getByRole("region", { name: "Tu as vu une lumière bouger dans le ciel ?" });
}

function touch(view: HTMLElement, name: string) {
  fireEvent.click(within(view).getByRole("button", { name }));
}

async function startAiming(view: HTMLElement) {
  await act(async () => {
    touch(view, AIM);
    await Promise.resolve();
  });
}

function theChosenDirection(view: HTMLElement) {
  const rose = within(view).getByRole("group", { name: "Dans quelle direction ?" });
  return within(rose)
    .queryAllByRole("button", { pressed: true })
    .map((button) => button.getAttribute("aria-label"));
}

describe("la page « C'était quoi ? »", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("cherche ce qui était dans la direction choisie au-dessus de l'observateur, et répond", async () => {
    const fetch = theApiAnswers(200, { candidates: [A_PASS], satellites_checked: true });
    const onFeedback = vi.fn();
    const view = aSightingPage(onFeedback);

    touch(view, "Est");
    touch(view, "Identifier");

    expect(await within(view).findByRole("heading", { level: 2, name: A_PASS.name })).toBeVisible();
    expect(fetch).toHaveBeenCalledWith(expect.stringMatching(/latitude=45.76&.*direction=E$/));
    touch(view, "Ce n'était pas ça ? Dis-le-nous");
    expect(onFeedback).toHaveBeenCalledTimes(1);
  });

  it("ne propose pas de viser sur un ordinateur", () => {
    expect(within(aSightingPage()).queryByRole("button", { name: AIM })).not.toBeInTheDocument();
  });

  it("choisit la direction que vise le téléphone, jusqu'à ce que le visiteur la choisisse lui-même", async () => {
    anAndroidPhone();
    const view = aSightingPage();

    await startAiming(view);
    theOrientationIs("deviceorientationabsolute", NORTH_EAST);
    expect(within(view).getByRole("status")).toHaveTextContent("Tu vises le nord-est");
    expect(theChosenDirection(view)).toEqual(["Nord-est"]);

    touch(view, "Sud");
    theOrientationIs("deviceorientationabsolute", NORTH_EAST);
    expect(theChosenDirection(view)).toEqual(["Sud"]);
    expect(within(view).getByRole("button", { name: AIM })).toBeVisible();
  });

  it("arrête de viser quand le visiteur demande à identifier", async () => {
    theApiAnswers(200, { candidates: [], satellites_checked: true });
    anAndroidPhone();
    const view = aSightingPage();
    await startAiming(view);
    theOrientationIs("deviceorientationabsolute", NORTH_EAST);

    touch(view, "Identifier");

    expect(within(view).getByRole("button", { name: AIM })).toBeVisible();
    await within(view).findByRole("heading", { level: 2, name: "Ni satellite ni planète" });
  });

  it("efface l'alerte quand le visiteur se met à viser, et dit pourquoi la visée s'arrête", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    anAndroidPhone();
    const view = aSightingPage();
    touch(view, "Identifier");
    const alert = within(view).getByRole("alert");
    expect(alert).toHaveTextContent("Choisis la direction où tu l'as vue.");

    await startAiming(view);
    expect(alert).toBeEmptyDOMElement();

    act(() => {
      vi.advanceTimersByTime(3000);
    });
    expect(alert).toHaveTextContent(
      "La boussole de ton téléphone ne répond pas : choisis la direction toi-même.",
    );
  });
});
