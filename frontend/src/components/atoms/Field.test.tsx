import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Field } from "./Field";

describe("un champ du formulaire", () => {
  it("est nommé par le libellé qui l'enveloppe", () => {
    render(
      <Field label="Ton message">
        <textarea />
      </Field>,
    );

    expect(screen.getByLabelText("Ton message").tagName).toBe("TEXTAREA");
  });
});
