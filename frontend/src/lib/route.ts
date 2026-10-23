// L'adresse de la page : chaque vue a son ancre, et « Ce soir » s'ouvre par défaut.

export type View = "tonight" | "sighting";

export const VIEW_ANCHORS: Record<View, string> = {
  tonight: "#ce-soir",
  sighting: "#cetait-quoi",
};

// L'ancre de l'ancien onglet « Ton avis », devenu une fenêtre.
const FEEDBACK_ANCHOR = "#avis";

export function viewOf(hash: string): View {
  return hash === VIEW_ANCHORS.sighting ? "sighting" : "tonight";
}

export function opensFeedback(hash: string): boolean {
  return hash === FEEDBACK_ANCHOR;
}
