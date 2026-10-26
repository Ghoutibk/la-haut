import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { PassDescription } from "../../lib/tonight";
import { PassCard } from "./PassCard";

const TIANGONG: PassDescription = {
  time: "21:42",
  day: null,
  name: "Station spatiale chinoise Tiangong",
  path: "sud → est · 4 min",
  peak: "Au plus haut à 17° au-dessus de l'horizon",
  explanation: null,
};

describe("un passage de ce soir", () => {
  it("se lit à son heure : nom, chemin et hauteur", () => {
    render(<PassCard pass={TIANGONG} />);
    const card = screen.getByRole("listitem");

    for (const text of [TIANGONG.time, TIANGONG.name, TIANGONG.path, TIANGONG.peak]) {
      expect(card).toHaveTextContent(text);
    }
  });

  it("donne son jour quand ce n'est pas aujourd'hui, et ce qu'il est quand il faut l'expliquer", () => {
    const explanation = "Une file de points brillants qui se suivent.";
    render(<PassCard pass={{ ...TIANGONG, day: "mardi 6 octobre", explanation }} />);

    expect(screen.getByText("mardi 6 octobre")).toBeVisible();
    expect(screen.getByText(explanation)).toBeVisible();
  });
});
