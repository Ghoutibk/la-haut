import { fireEvent, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { COMPASS_ROSE } from "../../lib/compass";
import type { SightingMoment } from "../../lib/sighting";
import { SightingForm, type SightingFormProps } from "./SightingForm";

const EARLIER_LABEL = "Heure à laquelle tu l'as vue";

function aForm(props: Partial<SightingFormProps> = {}) {
  const { container } = render(
    <SightingForm
      moment="now"
      onMoment={vi.fn()}
      earlier=""
      onEarlier={vi.fn()}
      direction={{
        rose: COMPASS_ROSE,
        chosen: null,
        onChoose: vi.fn(),
        aiming: {
          available: false,
          active: false,
          reading: "",
          onStart: vi.fn(),
          onDone: vi.fn(),
        },
      }}
      alert=""
      busy={false}
      onSubmit={vi.fn()}
      {...props}
    />,
  );
  return container.querySelector("form") as HTMLFormElement;
}

describe("le formulaire « C'était quoi, ça ? »", () => {
  it("laisse la page vérifier ce que le visiteur a rempli", () => {
    expect(aForm()).toHaveAttribute("novalidate");
  });

  it("demande quand, sans l'heure tant que la lumière n'a pas été vue plus tôt", async () => {
    const onMoment = vi.fn<(moment: SightingMoment) => void>();
    aForm({ onMoment });
    const when = screen.getByRole("group", { name: "Quand ?" });

    expect(within(when).getByRole("button", { name: "À l'instant", pressed: true })).toBeVisible();
    expect(within(when).getByLabelText(EARLIER_LABEL)).not.toBeVisible();
    await userEvent.click(within(when).getByRole("button", { name: "Il y a 15 min" }));
    await userEvent.click(within(when).getByRole("button", { name: "Plus tôt" }));
    expect(onMoment.mock.calls).toEqual([["fifteen-minutes-ago"], ["earlier"]]);
  });

  it("demande l'heure d'une lumière vue plus tôt, dans « Quand ? »", () => {
    const onEarlier = vi.fn();
    aForm({ moment: "earlier", onEarlier });
    const field = within(screen.getByRole("group", { name: "Quand ?" })).getByLabelText(
      EARLIER_LABEL,
    );

    fireEvent.change(field, { target: { value: "2026-10-05T19:05" } });

    expect(field).toBeVisible();
    expect(onEarlier).toHaveBeenCalledWith("2026-10-05T19:05");
  });

  it("demande la direction, alerte et patiente", () => {
    aForm({ alert: "Choisis la direction où tu l'as vue.", busy: true });

    expect(screen.getByRole("group", { name: "Dans quelle direction ?" })).toBeVisible();
    expect(screen.getByRole("alert")).toHaveTextContent("Choisis la direction où tu l'as vue.");
    expect(screen.getByRole("button", { name: "Identifier" })).toHaveAttribute("aria-busy", "true");
  });

  it("demande à identifier la lumière", async () => {
    const onSubmit = vi.fn();
    aForm({ onSubmit });

    await userEvent.click(screen.getByRole("button", { name: "Identifier" }));

    expect(onSubmit).toHaveBeenCalledTimes(1);
  });
});
