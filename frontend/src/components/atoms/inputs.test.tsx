import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { BotTrap } from "./BotTrap";
import { DateTimeInput, EmailInput, TextArea } from "./inputs";

describe("les champs de la page", () => {
  it("écrivent un message long, borné, avec un exemple", async () => {
    const onChange = vi.fn();
    render(<TextArea value="" onChange={onChange} maxLength={2000} placeholder="Par exemple" />);
    const message = screen.getByRole("textbox");

    await userEvent.type(message, "O");

    expect(onChange).toHaveBeenCalledWith("O");
    expect(message).toHaveAttribute("maxlength", "2000");
    expect(message).toHaveAttribute("placeholder", "Par exemple");
  });

  it("reçoivent un e-mail que le navigateur sait proposer", async () => {
    const onChange = vi.fn();
    render(<EmailInput value="" onChange={onChange} maxLength={254} />);
    const contact = screen.getByRole("textbox");

    await userEvent.type(contact, "c");

    expect(onChange).toHaveBeenCalledWith("c");
    expect(contact).toHaveAttribute("type", "email");
    expect(contact).toHaveAttribute("autocomplete", "email");
    expect(contact).toHaveAttribute("maxlength", "254");
  });

  it("reçoivent une date et une heure", () => {
    const onChange = vi.fn();
    const { container } = render(<DateTimeInput value="" onChange={onChange} />);
    const input = container.querySelector("input");

    fireEvent.change(input as HTMLInputElement, { target: { value: "2026-10-05T19:05" } });

    expect(input).toHaveAttribute("type", "datetime-local");
    expect(onChange).toHaveBeenCalledWith("2026-10-05T19:05");
  });
});

describe("le piège à robots", () => {
  it("se cache du lecteur d'écran et du clavier, mais reste un champ à remplir", () => {
    const onChange = vi.fn();
    const { container } = render(<BotTrap value="" onChange={onChange} />);
    const trap = container.firstElementChild;
    const input = container.querySelector("input");

    expect(trap?.tagName).toBe("DIV");
    expect(trap).toHaveAttribute("aria-hidden", "true");
    expect(trap).toHaveTextContent("Ne remplis pas ce champ");
    expect(input).toHaveAttribute("tabindex", "-1");
    expect(input).toHaveAttribute("autocomplete", "off");

    fireEvent.change(input as HTMLInputElement, { target: { value: "https://spam.example" } });
    expect(onChange).toHaveBeenCalledWith("https://spam.example");
  });
});
