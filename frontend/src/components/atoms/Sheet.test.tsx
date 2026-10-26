import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { Sheet } from "./Sheet";

// La fenêtre occupe le bas d'un écran de téléphone.
const THE_SHEET = { left: 0, right: 390, top: 300, bottom: 844 };

function aSheet(open: boolean, onClose = vi.fn()) {
  const view = render(
    <Sheet open={open} onClose={onClose} labelledBy="feedback-title">
      <h2 id="feedback-title">Un souci, une idée ?</h2>
      <button type="button">Envoyer</button>
    </Sheet>,
  );
  const dialog = view.container.querySelector("dialog") as HTMLDialogElement;
  dialog.getBoundingClientRect = () => THE_SHEET as DOMRect;
  return { ...view, dialog, onClose };
}

describe("la fenêtre posée sur la page", () => {
  it("s'ouvre en fenêtre, nommée par son titre, quand la page le demande", () => {
    aSheet(true);

    expect(screen.getByRole("dialog", { name: "Un souci, une idée ?" })).toHaveAttribute("open");
  });

  it("reste fermée, puis se ferme quand la page le demande", () => {
    const { dialog, rerender, onClose } = aSheet(false);
    expect(dialog.open).toBe(false);

    rerender(
      <Sheet open onClose={onClose} labelledBy="feedback-title">
        {null}
      </Sheet>,
    );
    expect(dialog.open).toBe(true);

    rerender(
      <Sheet open={false} onClose={onClose} labelledBy="feedback-title">
        {null}
      </Sheet>,
    );
    expect(dialog.open).toBe(false);
  });

  it("prévient la page quand le navigateur la ferme, par Échap par exemple", () => {
    const { dialog, onClose } = aSheet(true);

    dialog.close();

    expect(onClose).toHaveBeenCalled();
  });

  it("se ferme d'un toucher sur le fond assombri, hors d'elle", () => {
    const { dialog, onClose } = aSheet(true);

    fireEvent.click(dialog, { clientX: 200, clientY: THE_SHEET.top - 100 });

    expect(onClose).toHaveBeenCalled();
  });

  it("reste ouverte d'un toucher sur elle-même ou sur ce qu'elle contient", async () => {
    const { dialog, onClose } = aSheet(true);

    fireEvent.click(dialog, { clientX: 200, clientY: THE_SHEET.top + 10 });
    await userEvent.click(screen.getByRole("button", { name: "Envoyer" }));

    expect(onClose).not.toHaveBeenCalled();
  });

  it("reste ouverte quand un bouton est activé au clavier, sans coordonnées", async () => {
    const { onClose } = aSheet(true);

    screen.getByRole("button", { name: "Envoyer" }).focus();
    await userEvent.keyboard("{Enter}");

    expect(onClose).not.toHaveBeenCalled();
  });
});
