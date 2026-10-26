import { render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { A_PASS, A_PASS_DESCRIPTION, LYON, theApiAnswers } from "../../testing/doubles";
import { TonightPage } from "./TonightPage";

describe("la page « Ce soir »", () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date("2026-10-05T21:30:00+02:00"));
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("décrit les passages trouvés au-dessus de l'observateur", async () => {
    theApiAnswers(200, { passes: [A_PASS] });
    render(<TonightPage observer={LYON} hidden={false} />);
    const view = screen.getByRole("region", { name: "Au-dessus de toi" });

    const card = await within(view).findByRole("listitem");

    expect(card).toHaveTextContent(A_PASS_DESCRIPTION.path);
    expect(card).not.toHaveTextContent("lundi");
  });

  it("cherche encore tant que l'observateur n'est pas situé", () => {
    render(<TonightPage observer={null} hidden={false} />);

    expect(screen.getByRole("status")).toHaveTextContent("Recherche des passages…");
  });
});
