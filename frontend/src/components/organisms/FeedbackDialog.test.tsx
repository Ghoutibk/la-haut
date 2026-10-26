import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { aFeedbackDialog } from "../../testing/props";
import { FeedbackDialog, type FeedbackDialogProps } from "./FeedbackDialog";

const THANKS = "Bien reçu";

function aDialog(changes: Partial<FeedbackDialogProps> = {}) {
  render(<FeedbackDialog {...aFeedbackDialog(changes)} />);
}

describe("la fenêtre d'avis", () => {
  it("se nomme par son titre, hors du formulaire, et dit à qui écrire", () => {
    aDialog();
    const dialog = screen.getByRole("dialog", { name: "Un souci, une idée ?" });
    const title = screen.getByRole("heading", { level: 2, name: "Un souci, une idée ?" });

    expect(dialog).toHaveTextContent("Ton avis");
    expect(title.closest("form")).toBeNull();
    expect(
      screen.getByText(
        "Dis-nous ce qui ne marche pas ou ce qui te manquerait. Ton message n'est lu que par l'auteur du site.",
      ),
    ).toBeVisible();
  });

  it("montre le formulaire tant que rien n'est envoyé", () => {
    aDialog();

    expect(screen.getByRole("button", { name: "Envoyer" })).toBeVisible();
    expect(screen.getByText(THANKS)).not.toBeVisible();
  });

  it("remercie à la place du formulaire, et y revient", async () => {
    const onWriteAnother = vi.fn();
    aDialog({ thanked: true, onWriteAnother });

    expect(screen.getByText(THANKS)).toBeVisible();
    expect(screen.queryByRole("button", { name: "Envoyer" })).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Écrire un autre message" }));
    expect(onWriteAnother).toHaveBeenCalledTimes(1);
  });

  it("se ferme par sa croix", async () => {
    const onClose = vi.fn();
    aDialog({ onClose });

    await userEvent.click(screen.getByRole("button", { name: "Fermer" }));

    expect(onClose).toHaveBeenCalled();
  });
});
