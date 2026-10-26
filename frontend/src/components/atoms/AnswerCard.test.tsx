import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { AnswerCard } from "./AnswerCard";
import { ObserverMarker } from "./ObserverMarker";

describe("la carte d'une réponse", () => {
  it("est en place avant la réponse, pour l'annoncer sans interrompre", () => {
    const { container, rerender } = render(<AnswerCard>{null}</AnswerCard>);
    const card = container.firstElementChild;
    expect(card).toHaveAttribute("aria-live", "polite");
    expect(card).toBeEmptyDOMElement();

    rerender(
      <AnswerCard>
        <h2>Merci !</h2>
      </AnswerCard>,
    );
    expect(container.firstElementChild).toBe(card);
    expect(card).toHaveTextContent("Merci !");
  });

  it("peut rester cachée", () => {
    render(
      <AnswerCard hidden>
        <h2>Merci !</h2>
      </AnswerCard>,
    );

    expect(screen.queryByRole("heading")).not.toBeInTheDocument();
  });
});

describe("la personne au centre de la rose des vents", () => {
  it("se nomme « Toi », sans rien dire au lecteur d'écran", () => {
    render(<ObserverMarker />);

    expect(screen.getByText("Toi")).toHaveAttribute("aria-hidden", "true");
  });
});
