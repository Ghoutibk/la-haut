import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { A_PASS_DESCRIPTION } from "../../testing/doubles";
import { PassList } from "./PassList";

describe("les passages de ce soir", () => {
  it("annoncent ce que la vue a trouvé, puis chaque passage dans l'ordre", () => {
    const later = { ...A_PASS_DESCRIPTION, time: "05:49", day: "mardi 6 octobre" };
    render(<PassList status="Les satellites célèbres." passes={[A_PASS_DESCRIPTION, later]} />);

    expect(screen.getByRole("status")).toHaveTextContent("Les satellites célèbres.");
    const items = within(screen.getByRole("list")).getAllByRole("listitem");
    expect(items.map((item) => item.textContent)).toEqual([
      expect.stringContaining("21:42"),
      expect.stringContaining("05:49"),
    ]);
  });

  it("laissent une liste vide quand il n'y a rien à voir", () => {
    render(<PassList status="Recherche des passages…" passes={[]} />);

    expect(screen.queryAllByRole("listitem")).toEqual([]);
  });
});
