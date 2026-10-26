import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ChoiceGroup } from "./ChoiceGroup";
import { EarlierTimeField } from "./EarlierTimeField";

const KINDS = [
  { value: "problem", label: "Un problème" },
  { value: "idea", label: "Une idée" },
] as const;

describe("l'heure d'une lumière vue plus tôt", () => {
  it("se demande quand le visiteur l'a vue « Plus tôt », ou se cache", () => {
    const { rerender } = render(<EarlierTimeField value="" onChange={vi.fn()} hidden={false} />);
    expect(screen.getByLabelText("Heure à laquelle tu l'as vue")).toBeVisible();

    rerender(<EarlierTimeField value="" onChange={vi.fn()} hidden />);
    expect(screen.queryByLabelText("Heure à laquelle tu l'as vue")).not.toBeVisible();
  });
});

describe("un groupe de choix", () => {
  it("se nomme par sa légende et ne fait qu'un choix à la fois", () => {
    render(<ChoiceGroup legend="C'est plutôt…" choices={KINDS} chosen="idea" onChoose={vi.fn()} />);
    const group = screen.getByRole("group", { name: "C'est plutôt…" });

    expect(within(group).getAllByRole("button", { pressed: true })).toEqual([
      within(group).getByRole("button", { name: "Une idée" }),
    ]);
    expect(
      within(group).getByRole("button", { name: "Un problème", pressed: false }),
    ).toBeVisible();
  });

  it("dit quel choix le visiteur touche", async () => {
    const onChoose = vi.fn();
    render(
      <ChoiceGroup legend="C'est plutôt…" choices={KINDS} chosen="idea" onChoose={onChoose} />,
    );

    await userEvent.click(screen.getByRole("button", { name: "Un problème" }));

    expect(onChoose).toHaveBeenCalledWith("problem");
  });

  it("place sous les choix ce qui les complète", () => {
    render(
      <ChoiceGroup legend="Quand ?" choices={KINDS} chosen="idea" onChoose={vi.fn()}>
        <p>Après les choix</p>
      </ChoiceGroup>,
    );
    const group = screen.getByRole("group", { name: "Quand ?" });

    expect(group.lastElementChild).toHaveTextContent("Après les choix");
  });
});
