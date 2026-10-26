import { render, screen } from "@testing-library/react";
import type { SyntheticEvent } from "react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { Chip, ChipButton } from "./Chip";
import { ChoiceButton, CloseButton, LinkButton, OutlineButton, PrimaryButton } from "./buttons";

describe("les boutons de la page", () => {
  it.each([
    ["la puce", ChipButton],
    ["le choix", ChoiceButton],
    ["le bouton cerné", OutlineButton],
    ["le lien", LinkButton],
  ])("%s ne soumet pas le formulaire où il est posé, et répond au toucher", async (_, Button) => {
    const onClick = vi.fn();
    const onSubmit = vi.fn();
    render(
      <form onSubmit={onSubmit}>
        <Button onClick={onClick}>Avis</Button>
      </form>,
    );

    await userEvent.click(screen.getByRole("button", { name: "Avis" }));

    expect(onClick).toHaveBeenCalledTimes(1);
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("annonce la fenêtre qu'ouvre une puce", () => {
    render(
      <ChipButton onClick={vi.fn()} opensDialog>
        Avis
      </ChipButton>,
    );

    expect(screen.getByRole("button", { name: "Avis" })).toHaveAttribute("aria-haspopup", "dialog");
  });

  it("dit si un choix est fait, seulement quand il fait partie d'un groupe", () => {
    render(
      <>
        <ChoiceButton onClick={vi.fn()} pressed>
          À l'instant
        </ChoiceButton>
        <ChoiceButton onClick={vi.fn()} pressed={false}>
          Plus tôt
        </ChoiceButton>
        <ChoiceButton onClick={vi.fn()}>C'est là</ChoiceButton>
      </>,
    );

    expect(screen.getByRole("button", { name: "À l'instant", pressed: true })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Plus tôt", pressed: false })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "C'est là" })).not.toHaveAttribute("aria-pressed");
  });

  it("nomme en toutes lettres un choix abrégé", () => {
    render(
      <ChoiceButton onClick={vi.fn()} pressed={false} shape="rose" label="Nord-ouest">
        NO
      </ChoiceButton>,
    );

    expect(screen.getByRole("button", { name: "Nord-ouest" })).toHaveTextContent("NO");
  });

  it("soumet le formulaire par le bouton principal, qui dit quand il travaille", async () => {
    const onSubmit = vi.fn((event: SyntheticEvent) => {
      event.preventDefault();
    });
    const { rerender } = render(
      <form onSubmit={onSubmit}>
        <PrimaryButton busy={false}>Identifier</PrimaryButton>
      </form>,
    );
    const button = screen.getByRole("button", { name: "Identifier" });
    expect(button).not.toHaveAttribute("aria-busy");

    await userEvent.click(button);
    expect(onSubmit).toHaveBeenCalledTimes(1);

    rerender(
      <form onSubmit={onSubmit}>
        <PrimaryButton busy>Identifier</PrimaryButton>
      </form>,
    );
    expect(button).toHaveAttribute("aria-busy", "true");
  });

  it("ferme par une croix nommée « Fermer »", async () => {
    const onClick = vi.fn();
    render(<CloseButton onClick={onClick} />);

    const close = screen.getByRole("button", { name: "Fermer" });
    expect(close).toHaveTextContent("×");
    await userEvent.click(close);
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("pose une puce qui n'est pas un bouton", () => {
    render(<Chip>Paris</Chip>);

    expect(screen.getByText("Paris")).toBeInTheDocument();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
});
