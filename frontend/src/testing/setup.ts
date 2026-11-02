// Les assertions du DOM (toBeVisible, toHaveAttribute…) pour Vitest, et un DOM vidé après chaque test.
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(cleanup);

// jsdom connaît <dialog> mais ne sait ni l'ouvrir en fenêtre ni la fermer : comme un navigateur,
// la fermeture prévient la page par l'événement « close ».
HTMLDialogElement.prototype.showModal = function showModal(this: HTMLDialogElement) {
  this.open = true;
};
HTMLDialogElement.prototype.close = function close(this: HTMLDialogElement) {
  this.open = false;
  this.dispatchEvent(new Event("close"));
};

// jsdom ne fait jamais défiler la page : un élément peut demander à venir à l'écran, rien ne bouge.
Element.prototype.scrollIntoView = function scrollIntoView() {
  // Rien à faire défiler.
};

// jsdom ne sait rien de l'écran : par défaut, celui d'un ordinateur, avec une souris.
window.matchMedia = ((query: string) => ({
  matches: query === "(pointer: fine)",
})) as unknown as typeof window.matchMedia;
