import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ViewSection } from "./ViewSection";

describe("une vue de la page", () => {
  it("se nomme par son titre, sous son surtitre", () => {
    render(
      <ViewSection eyebrow="Ce soir" title="Au-dessus de toi" hidden={false}>
        <p>Les passages</p>
      </ViewSection>,
    );
    const view = screen.getByRole("region", { name: "Au-dessus de toi" });

    expect(view).toHaveTextContent("Ce soir");
    expect(screen.getByRole("heading", { level: 1, name: "Au-dessus de toi" })).toBeVisible();
    expect(view).toHaveTextContent("Les passages");
  });

  it("se cache quand une autre vue est affichée", () => {
    render(
      <ViewSection eyebrow="Ce soir" title="Au-dessus de toi" hidden>
        {null}
      </ViewSection>,
    );

    expect(screen.queryByRole("region")).not.toBeInTheDocument();
    expect(screen.getByText("Au-dessus de toi", { selector: "h1" })).not.toBeVisible();
  });
});
