import { describe, expect, it } from "vitest";

import { fromThe, theDirection, towardThe } from "./french";

describe("les élisions devant une direction", () => {
  it("dit d'où vient la lumière", () => {
    expect(["sud", "nord-est", "ouest", "est"].map(fromThe)).toEqual([
      "du sud",
      "du nord-est",
      "de l'ouest",
      "de l'est",
    ]);
  });

  it("dit vers où elle va", () => {
    expect(["sud", "nord-ouest", "ouest", "est"].map(towardThe)).toEqual([
      "vers le sud",
      "vers le nord-ouest",
      "vers l'ouest",
      "vers l'est",
    ]);
  });

  it("nomme la direction visée", () => {
    expect(["nord", "sud-est", "est", "ouest"].map(theDirection)).toEqual([
      "le nord",
      "le sud-est",
      "l'est",
      "l'ouest",
    ]);
  });
});
