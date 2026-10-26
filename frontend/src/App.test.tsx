import { act, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";
import { theApiAnswers } from "./testing/doubles";

const TONIGHT = "Au-dessus de toi";
const SIGHTING = "Tu as vu une lumière bouger dans le ciel ?";
const FEEDBACK = "Un souci, une idée ?";

function theAddressIs(hash: string) {
  window.history.replaceState(null, "", `/${hash}`);
}

// Fermée, la fenêtre est cachée : elle se trouve sans son nom, qui se lit une fois ouverte.
function theFeedbackWindow() {
  return screen.getByRole("dialog", { hidden: true });
}

describe("la page de Là-haut", () => {
  beforeEach(() => {
    theApiAnswers(200, { passes: [] });
  });

  afterEach(() => {
    theAddressIs("");
    vi.unstubAllGlobals();
  });

  it("ouvre « Ce soir » par défaut, au-dessus de Paris quand le navigateur ne sait pas localiser", async () => {
    render(<App />);

    expect(screen.getByRole("region", { name: TONIGHT })).toBeVisible();
    expect(screen.queryByRole("region", { name: SIGHTING })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Ce soir" })).toHaveAttribute("aria-current", "page");
    expect(screen.getByRole("banner")).toHaveTextContent("Paris");
    expect(await screen.findByText(/Aucun passage visible/)).toBeVisible();
  });

  it("ouvre la vue de l'ancre de l'adresse, et la suit", async () => {
    theAddressIs("#cetait-quoi");
    render(<App />);
    expect(screen.getByRole("region", { name: SIGHTING })).toBeVisible();

    await act(async () => {
      window.location.hash = "#ce-soir";
      await new Promise((resolve) => setTimeout(resolve));
    });
    expect(screen.getByRole("region", { name: TONIGHT })).toBeVisible();
  });

  it("ouvre la fenêtre d'avis au chargement de l'ancienne adresse #avis, mais pas après", async () => {
    theAddressIs("#avis");
    const { unmount } = render(<App />);
    expect(screen.getByRole("dialog", { name: FEEDBACK })).toHaveAttribute("open");
    unmount();

    theAddressIs("#cetait-quoi");
    render(<App />);
    await act(async () => {
      window.location.hash = "#avis";
      await new Promise((resolve) => setTimeout(resolve));
    });
    expect(theFeedbackWindow()).not.toHaveAttribute("open");
  });

  it("ouvre la fenêtre d'avis par le bouton « Avis », et la ferme", async () => {
    render(<App />);

    await userEvent.click(within(screen.getByRole("banner")).getByRole("button", { name: "Avis" }));
    expect(theFeedbackWindow()).toHaveAttribute("open");

    await userEvent.click(screen.getByRole("button", { name: "Fermer" }));
    expect(theFeedbackWindow()).not.toHaveAttribute("open");
  });

  it("ouvre la fenêtre d'avis depuis une réponse qui n'était pas la bonne", async () => {
    theAddressIs("#cetait-quoi");
    render(<App />);
    await screen.findByText(/Aucun passage visible/);
    theApiAnswers(200, { candidates: [], satellites_checked: true });

    await userEvent.click(screen.getByRole("button", { name: "Nord" }));
    await userEvent.click(screen.getByRole("button", { name: "Identifier" }));
    await userEvent.click(
      await screen.findByRole("button", { name: "Ce n'était pas ça ? Dis-le-nous" }),
    );

    expect(theFeedbackWindow()).toHaveAttribute("open");
  });
});
