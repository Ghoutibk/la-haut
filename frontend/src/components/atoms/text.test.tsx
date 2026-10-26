import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ErrorText } from "./ErrorText";
import { Eyebrow } from "./Eyebrow";
import { Hint } from "./Hint";
import { Lede } from "./Lede";
import { Sentence } from "./Sentence";
import { Title } from "./Title";

describe("les textes de la page", () => {
  it("titrent au niveau demandé", () => {
    render(
      <>
        <Title level={1}>Au-dessus de toi</Title>
        <Title level={2} id="feedback-title">
          Un souci, une idée ?
        </Title>
      </>,
    );

    expect(screen.getByRole("heading", { level: 1, name: "Au-dessus de toi" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 2, name: "Un souci, une idée ?" })).toHaveAttribute(
      "id",
      "feedback-title",
    );
  });

  it("surtitrent, expliquent et précisent en paragraphes", () => {
    render(
      <>
        <Eyebrow>Ce soir</Eyebrow>
        <Hint>Repère : le Soleil se lève vers l'est.</Hint>
        <Sentence>Visible de 21:12 à 21:16.</Sentence>
      </>,
    );

    for (const text of [
      "Ce soir",
      "Repère : le Soleil se lève vers l'est.",
      "Visible de 21:12 à 21:16.",
    ]) {
      expect(screen.getByText(text).tagName).toBe("P");
    }
  });

  it("annoncent ce que la vue dit d'elle-même, quand on le leur demande", () => {
    render(
      <>
        <Lede>Dis-nous ce qui ne marche pas.</Lede>
        <Lede announces>Recherche des passages…</Lede>
      </>,
    );

    expect(screen.getByRole("status")).toHaveTextContent("Recherche des passages…");
  });

  it("gardent la place de l'alerte, même vide", () => {
    const { rerender } = render(<ErrorText>{""}</ErrorText>);
    expect(screen.getByRole("alert")).toBeEmptyDOMElement();

    rerender(<ErrorText>Choisis la direction où tu l'as vue.</ErrorText>);
    expect(screen.getByRole("alert")).toHaveTextContent("Choisis la direction où tu l'as vue.");
  });
});
