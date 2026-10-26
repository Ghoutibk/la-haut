import { useSyncExternalStore } from "react";

import { type View, viewOf } from "../lib/route";

function subscribe(onChange: () => void): () => void {
  window.addEventListener("hashchange", onChange);
  return () => {
    window.removeEventListener("hashchange", onChange);
  };
}

// La vue que l'ancre de l'adresse ouvre, tenue à jour quand l'ancre change.
export function useHashView(): View {
  return useSyncExternalStore(subscribe, () => viewOf(window.location.hash));
}
