import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { AimButton } from "./AimButton";
import { AimingPanel } from "./AimingPanel";

describe("viser avec le téléphone", () => {
  it("commence par le bouton « Viser avec mon téléphone »", async () => {
    const onClick = vi.fn();
    render(<AimButton onClick={onClick} />);

    await userEvent.click(screen.getByRole("button", { name: "Viser avec mon téléphone" }));

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it("explique comment tenir le téléphone, annonce la visée et s'arrête à « C'est là »", async () => {
    const onDone = vi.fn();
    render(<AimingPanel reading="Tu vises le nord-est" onDone={onDone} />);

    expect(
      screen.getByText(
        "Tiens ton téléphone à plat devant toi et tourne-toi : le haut de l'écran doit pointer vers l'endroit où tu as vu la lumière.",
      ),
    ).toBeVisible();
    expect(screen.getByRole("status")).toHaveTextContent("Tu vises le nord-est");

    await userEvent.click(screen.getByRole("button", { name: "C'est là" }));
    expect(onDone).toHaveBeenCalledTimes(1);
  });
});
