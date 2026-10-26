import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { COMPASS_ROSE } from "../../lib/compass";
import { CompassRose } from "./CompassRose";

describe("la rose des vents", () => {
  it("entoure le visiteur des huit directions, abrégées et nommées en toutes lettres", () => {
    const { container } = render(
      <CompassRose rose={COMPASS_ROSE} chosen={null} onChoose={vi.fn()} />,
    );

    const cells = container.querySelectorAll(":scope > div > *");

    expect([...cells].map((cell) => cell.textContent)).toEqual([
      "NO",
      "N",
      "NE",
      "O",
      "Toi",
      "E",
      "SO",
      "S",
      "SE",
    ]);
    expect(screen.getByRole("button", { name: "Nord-ouest" })).toHaveTextContent("NO");
    expect(screen.queryAllByRole("button", { pressed: true })).toEqual([]);
  });

  it("montre la direction choisie, et dit laquelle le visiteur touche", async () => {
    const onChoose = vi.fn();
    render(<CompassRose rose={COMPASS_ROSE} chosen="SE" onChoose={onChoose} />);

    expect(screen.getAllByRole("button", { pressed: true })).toEqual([
      screen.getByRole("button", { name: "Sud-est" }),
    ]);

    await userEvent.click(screen.getByRole("button", { name: "Ouest" }));
    expect(onChoose).toHaveBeenCalledWith("W");
  });
});
