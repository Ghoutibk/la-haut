import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { VIEW_ANCHORS } from "../../lib/route";
import { aFeedbackDialog } from "../../testing/props";
import { MobileShell } from "./MobileShell";

describe("la page sur un téléphone", () => {
  it("pose l'en-tête, les vues, les onglets et la fenêtre d'avis", () => {
    render(
      <MobileShell
        topBar={{ place: "Paris", onFeedback: vi.fn() }}
        tabBar={{ anchors: VIEW_ANCHORS, current: "tonight" }}
        feedback={aFeedbackDialog({ open: false })}
      >
        <p>Les vues</p>
      </MobileShell>,
    );

    expect(screen.getByRole("banner")).toHaveTextContent("Paris");
    expect(screen.getByRole("main")).toHaveTextContent("Les vues");
    expect(screen.getByRole("navigation", { name: "Navigation principale" })).toBeVisible();
    expect(screen.getByRole("dialog", { hidden: true })).not.toHaveAttribute("open");
  });
});
