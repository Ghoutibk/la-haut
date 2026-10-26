import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { Brand } from "./Brand";
import { FeedbackButton } from "./FeedbackButton";
import { PlaceChip } from "./PlaceChip";

describe("l'en-tête de la page", () => {
  it("porte le nom de Là-haut", () => {
    render(<Brand />);

    expect(screen.getByText("Là-haut")).toBeInTheDocument();
  });

  it("dit d'où le visiteur regarde le ciel", () => {
    render(<PlaceChip place="Ta position" />);

    expect(screen.getByText("Ta position")).toBeInTheDocument();
  });

  it("ouvre la fenêtre d'avis par le bouton « Avis »", async () => {
    const onClick = vi.fn();
    render(<FeedbackButton onClick={onClick} />);
    const button = screen.getByRole("button", { name: "Avis" });

    await userEvent.click(button);

    expect(button).toHaveAttribute("aria-haspopup", "dialog");
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
