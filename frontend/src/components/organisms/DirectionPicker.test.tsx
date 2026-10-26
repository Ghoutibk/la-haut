import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { aDirectionPicker, anAiming } from "../../testing/props";
import { type AimingProps, DirectionPicker } from "./DirectionPicker";

const AIM = "Viser avec mon téléphone";
const OR_CHOOSE = "Ou choisis la direction toi-même :";

function aPicker(aiming: Partial<AimingProps> = {}, onChoose = vi.fn()) {
  render(
    <DirectionPicker {...aDirectionPicker({ chosen: "N", onChoose, aiming: anAiming(aiming) })} />,
  );
  return screen.getByRole("group", { name: "Dans quelle direction ?" });
}

describe("le choix de la direction", () => {
  it("propose la rose des vents et un repère, sans visée sur un ordinateur", async () => {
    const onChoose = vi.fn();
    const group = aPicker({}, onChoose);

    expect(within(group).getByRole("button", { name: "Nord", pressed: true })).toBeVisible();
    expect(group).toHaveTextContent(
      "Repère : le Soleil se lève vers l'est et se couche vers l'ouest.",
    );
    expect(within(group).queryByRole("button", { name: AIM })).not.toBeInTheDocument();
    expect(within(group).queryByText(OR_CHOOSE)).not.toBeInTheDocument();

    await userEvent.click(within(group).getByRole("button", { name: "Sud" }));
    expect(onChoose).toHaveBeenCalledWith("S");
  });

  it("propose de viser sur un téléphone qui a une boussole", async () => {
    const onStart = vi.fn();
    const group = aPicker({ available: true, onStart });

    expect(within(group).getByText(OR_CHOOSE)).toBeVisible();
    expect(within(group).queryByRole("status")).not.toBeInTheDocument();
    await userEvent.click(within(group).getByRole("button", { name: AIM }));
    expect(onStart).toHaveBeenCalledTimes(1);
  });

  it("suit la visée à la place du bouton, jusqu'à « C'est là »", async () => {
    const onDone = vi.fn();
    const group = aPicker({ available: true, active: true, reading: "Tu vises le nord", onDone });

    expect(within(group).queryByRole("button", { name: AIM })).not.toBeInTheDocument();
    expect(within(group).getByRole("status")).toHaveTextContent("Tu vises le nord");
    expect(within(group).getByText(OR_CHOOSE)).toBeVisible();
    await userEvent.click(within(group).getByRole("button", { name: "C'est là" }));
    expect(onDone).toHaveBeenCalledTimes(1);
  });
});
