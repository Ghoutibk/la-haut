import { fireEvent, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import type { FeedbackDraft } from "../../lib/feedback";
import { FeedbackForm, type FeedbackFormProps } from "./FeedbackForm";

const MESSAGE = "Ton message";
const CONTACT = "Ton e-mail, si tu veux une réponse (facultatif)";
const A_DRAFT: FeedbackDraft = { kind: "idea", message: "", contact: "", website: "" };

function aForm(props: Partial<FeedbackFormProps> = {}) {
  const { container } = render(
    <FeedbackForm
      draft={A_DRAFT}
      onRevise={vi.fn()}
      alert=""
      busy={false}
      onSend={vi.fn()}
      hidden={false}
      {...props}
    />,
  );
  return container.querySelector("form") as HTMLFormElement;
}

describe("le formulaire « Ton avis »", () => {
  it("laisse la page vérifier le message", () => {
    expect(aForm()).toHaveAttribute("novalidate");
  });

  it("demande de quelle nature est l'avis", async () => {
    const onRevise = vi.fn();
    aForm({ onRevise });
    const kinds = screen.getByRole("group", { name: "C'est plutôt…" });

    expect(within(kinds).getByRole("button", { name: "Une idée", pressed: true })).toBeVisible();
    await userEvent.click(within(kinds).getByRole("button", { name: "Autre chose" }));
    await userEvent.click(within(kinds).getByRole("button", { name: "Un problème" }));
    expect(onRevise.mock.calls).toEqual([[{ kind: "other" }], [{ kind: "problem" }]]);
  });

  it("demande le message, et l'e-mail sans l'exiger", () => {
    const onRevise = vi.fn();
    aForm({ onRevise, draft: { ...A_DRAFT, message: "Merci", contact: "claire@" } });
    const message = screen.getByLabelText(MESSAGE);
    const contact = screen.getByLabelText(CONTACT);

    expect(message).toHaveValue("Merci");
    expect(message).toHaveAttribute("maxlength", "2000");
    expect(message).toHaveAttribute(
      "placeholder",
      "Par exemple : la boussole ne bouge pas sur mon téléphone.",
    );
    expect(contact).toHaveValue("claire@");
    expect(contact).toHaveAttribute("maxlength", "254");
    expect(
      screen.getByText("Ton e-mail ne sert qu'à te répondre. Il n'est jamais affiché sur le site."),
    ).toBeVisible();

    fireEvent.change(message, { target: { value: "Merci !" } });
    fireEvent.change(contact, { target: { value: "claire@example.org" } });
    expect(onRevise.mock.calls).toEqual([
      [{ message: "Merci !" }],
      [{ contact: "claire@example.org" }],
    ]);
  });

  it("tend le piège aux robots", () => {
    const onRevise = vi.fn();
    const form = aForm({ onRevise });

    fireEvent.change(within(form).getByLabelText("Ne remplis pas ce champ"), {
      target: { value: "https://spam.example" },
    });

    expect(onRevise).toHaveBeenCalledWith({ website: "https://spam.example" });
  });

  it("alerte, patiente et envoie", async () => {
    const onSend = vi.fn();
    aForm({ onSend, alert: "Écris ton message avant de l'envoyer.", busy: true });

    expect(screen.getByRole("alert")).toHaveTextContent("Écris ton message avant de l'envoyer.");
    const send = screen.getByRole("button", { name: "Envoyer" });
    expect(send).toHaveAttribute("aria-busy", "true");
    await userEvent.click(send);
    expect(onSend).toHaveBeenCalledTimes(1);
  });

  it("se cache pendant le remerciement", () => {
    expect(aForm({ hidden: true })).not.toBeVisible();
  });
});
