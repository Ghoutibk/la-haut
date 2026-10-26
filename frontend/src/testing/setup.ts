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
