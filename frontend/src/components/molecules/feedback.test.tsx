import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { FeedbackLink } from "./FeedbackLink";
import { FeedbackThanks } from "./FeedbackThanks";
import { SheetHeader } from "./SheetHeader";

describe("la fenêtre d'avis", () => {
  it("se surtitre et se ferme par sa croix", async () => {
    const onClose = vi.fn();
    render(<SheetHeader eyebrow="Ton avis" onClose={onClose} />);

    expect(screen.getByText("Ton avis")).toBeVisible();
    await userEvent.click(screen.getByRole("button", { name: "Fermer" }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("s'ouvre depuis une réponse qui n'était pas la bonne", async () => {
    const onClick = vi.fn();
    render(<FeedbackLink onClick={onClick} />);

    await userEvent.click(screen.getByRole("button", { name: "Ce n'était pas ça ? Dis-le-nous" }));

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("remercie de l'avis reçu, et propose d'en écrire un autre", async () => {
    const onWriteAnother = vi.fn();
    render(<FeedbackThanks hidden={false} onWriteAnother={onWriteAnother} />);

    expect(screen.getByText("Bien reçu")).toBeVisible();
    expect(screen.getByRole("heading", { level: 2, name: "Merci !" })).toBeVisible();
    expect(
      screen.getByText(
        "Ton message est arrivé chez l'auteur du site. Si tu as laissé ton e-mail, il pourra te répondre.",
      ),
    ).toBeVisible();
    await userEvent.click(screen.getByRole("button", { name: "Écrire un autre message" }));
    expect(onWriteAnother).toHaveBeenCalledTimes(1);
  });

  it("garde son remerciement caché tant que rien n'est reçu", () => {
    render(<FeedbackThanks hidden onWriteAnother={vi.fn()} />);

    expect(screen.queryByText("Bien reçu")).not.toBeVisible();
  });
});
