import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { TabLink } from "./TabLink";

describe("un onglet de la page", () => {
  it("mène à l'ancre de sa vue, et dit quand c'est la vue affichée", () => {
    render(
      <>
        <TabLink href="#ce-soir" label="Ce soir" icon={<svg />} current />
        <TabLink href="#cetait-quoi" label="C'était quoi ?" icon={<svg />} current={false} />
      </>,
    );

    const tonight = screen.getByRole("link", { name: "Ce soir" });
    const sighting = screen.getByRole("link", { name: "C'était quoi ?" });
    expect(tonight).toHaveAttribute("href", "#ce-soir");
    expect(tonight).toHaveAttribute("aria-current", "page");
    expect(sighting).not.toHaveAttribute("aria-current");
  });
});
