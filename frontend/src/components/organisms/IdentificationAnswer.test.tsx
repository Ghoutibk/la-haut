import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import type { Answer } from "../../lib/identification";
import { IdentificationAnswer } from "./IdentificationAnswer";

const AN_ANSWER: Answer = {
  eyebrow: "C'était très probablement",
  title: "Vénus",
  sentences: [
    "Vénus brillait vers l'ouest, à 12° au-dessus de l'horizon.",
    "Ou peut-être : Jupiter.",
  ],
};

describe("la réponse à « C'était quoi, ça ? »", () => {
  it("attend la réponse dans une région annoncée sans interrompre", () => {
    const { container } = render(<IdentificationAnswer answer={null} onFeedback={vi.fn()} />);

    expect(container.firstElementChild).toHaveAttribute("aria-live", "polite");
    expect(container.firstElementChild).toBeEmptyDOMElement();
  });

  it("nomme ce que c'était, sous son surtitre, en phrases", () => {
    render(<IdentificationAnswer answer={AN_ANSWER} onFeedback={vi.fn()} />);

    expect(screen.getByText("C'était très probablement")).toBeVisible();
    expect(screen.getByRole("heading", { level: 2, name: "Vénus" })).toBeVisible();
    for (const sentence of AN_ANSWER.sentences) expect(screen.getByText(sentence)).toBeVisible();
  });

  it("propose de dire que ce n'était pas ça", async () => {
    const onFeedback = vi.fn();
    render(<IdentificationAnswer answer={AN_ANSWER} onFeedback={onFeedback} />);

    await userEvent.click(screen.getByRole("button", { name: "Ce n'était pas ça ? Dis-le-nous" }));

    expect(onFeedback).toHaveBeenCalledTimes(1);
  });
});
