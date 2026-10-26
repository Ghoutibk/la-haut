import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { VIEW_ANCHORS } from "../../lib/route";
import { TabBar } from "./TabBar";
import { TopBar } from "./TopBar";

describe("la barre du haut", () => {
  it("porte le nom de Là-haut, le lieu du visiteur et le bouton « Avis »", async () => {
    const onFeedback = vi.fn();
    render(<TopBar place="Paris" onFeedback={onFeedback} />);
    const header = screen.getByRole("banner");

    expect(header).toHaveTextContent("Là-haut");
    expect(header).toHaveTextContent("Paris");
    await userEvent.click(within(header).getByRole("button", { name: "Avis" }));
    expect(onFeedback).toHaveBeenCalledTimes(1);
  });
});

describe("la barre des onglets", () => {
  it("mène à chaque vue par son ancre et marque la vue affichée", () => {
    render(<TabBar anchors={VIEW_ANCHORS} current="sighting" />);
    const navigation = screen.getByRole("navigation", { name: "Navigation principale" });
    const tonight = within(navigation).getByRole("link", { name: "Ce soir" });
    const sighting = within(navigation).getByRole("link", { name: "C'était quoi ?" });

    expect(tonight).toHaveAttribute("href", "#ce-soir");
    expect(tonight).not.toHaveAttribute("aria-current");
    expect(sighting).toHaveAttribute("href", "#cetait-quoi");
    expect(sighting).toHaveAttribute("aria-current", "page");
  });
});
