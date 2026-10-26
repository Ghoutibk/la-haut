import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Fieldset } from "./Fieldset";

describe("une question du formulaire", () => {
  it("nomme le groupe de ses réponses par sa légende", () => {
    render(
      <Fieldset legend="Dans quelle direction ?">
        <button type="button">Nord</button>
      </Fieldset>,
    );

    expect(screen.getByRole("group", { name: "Dans quelle direction ?" })).toContainElement(
      screen.getByRole("button", { name: "Nord" }),
    );
  });
});
