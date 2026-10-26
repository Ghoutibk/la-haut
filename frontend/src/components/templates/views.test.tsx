import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { A_PASS_DESCRIPTION } from "../../testing/doubles";
import { aSightingForm } from "../../testing/props";
import { SightingView } from "./SightingView";
import { TonightView } from "./TonightView";

describe("la vue « Ce soir »", () => {
  it("annonce les passages au-dessus du visiteur", () => {
    render(<TonightView hidden={false} status="Les satellites." passes={[A_PASS_DESCRIPTION]} />);
    const view = screen.getByRole("region", { name: "Au-dessus de toi" });

    expect(view).toHaveTextContent("Ce soir");
    expect(within(view).getByRole("status")).toHaveTextContent("Les satellites.");
    expect(within(view).getAllByRole("listitem")).toHaveLength(1);
  });
});

describe("la vue « C'était quoi ? »", () => {
  it("demande ce que le visiteur a vu, puis lui répond", () => {
    render(
      <SightingView
        hidden={false}
        form={aSightingForm()}
        answer={{ eyebrow: "Rien de connu", title: "Pas une planète", sentences: [] }}
        onFeedback={vi.fn()}
      />,
    );
    const view = screen.getByRole("region", { name: "Tu as vu une lumière bouger dans le ciel ?" });

    expect(view).toHaveTextContent("C'était quoi, ça ?");
    expect(within(view).getByRole("button", { name: "Identifier" })).toBeVisible();
    expect(within(view).getByRole("heading", { level: 2, name: "Pas une planète" })).toBeVisible();
  });
});
