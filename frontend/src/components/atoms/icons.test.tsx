import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CompassIcon, MoonIcon, OrbitIcon, PinIcon, SpeechBubbleIcon, TargetIcon } from "./icons";

describe("les icônes de la page", () => {
  it.each([
    ["l'orbite", OrbitIcon, 22],
    ["l'épingle", PinIcon, 14],
    ["la bulle", SpeechBubbleIcon, 14],
    ["la boussole", CompassIcon, 20],
    ["la lune", MoonIcon, 22],
    ["la cible", TargetIcon, 22],
  ])("dessinent %s sans rien dire au lecteur d'écran", (_, Icon, size) => {
    const { container } = render(<Icon />);
    const svg = container.querySelector("svg");

    expect(svg).toHaveAttribute("aria-hidden", "true");
    expect(svg).toHaveAttribute("width", String(size));
    expect(svg?.childElementCount).toBeGreaterThan(0);
  });
});
