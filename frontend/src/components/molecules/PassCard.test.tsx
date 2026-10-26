import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { A_PASS_DESCRIPTION } from "../../testing/doubles";
import { PassCard } from "./PassCard";

describe("un passage de ce soir", () => {
  it("se lit à son heure : nom, chemin et hauteur", () => {
    render(<PassCard pass={A_PASS_DESCRIPTION} />);
    const card = screen.getByRole("listitem");

    for (const text of [
      A_PASS_DESCRIPTION.time,
      A_PASS_DESCRIPTION.name,
      A_PASS_DESCRIPTION.path,
      A_PASS_DESCRIPTION.peak,
    ]) {
      expect(card).toHaveTextContent(text);
    }
  });

  it("donne son jour quand ce n'est pas aujourd'hui, et ce qu'il est quand il faut l'expliquer", () => {
    const explanation = "Une file de points brillants qui se suivent.";
    render(<PassCard pass={{ ...A_PASS_DESCRIPTION, day: "mardi 6 octobre", explanation }} />);

    expect(screen.getByText("mardi 6 octobre")).toBeVisible();
    expect(screen.getByText(explanation)).toBeVisible();
  });
});
