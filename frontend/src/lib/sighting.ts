// Le signalement d'une lumière : quand le visiteur l'a vue, et dans quelle direction.

import type { Sighting } from "./api";
import type { CompassPoint } from "./compass";
import { CHOOSE_DIRECTION, GIVE_TIME } from "./texts";

const FIFTEEN_MINUTES_MS = 15 * 60 * 1000;

export type SightingMoment = "now" | "fifteen-minutes-ago" | "earlier";

// Ce que le visiteur a rempli : « Quand ? », l'heure s'il l'a vue plus tôt, et la direction.
export interface SightingReport {
  readonly moment: SightingMoment;
  // La valeur d'un champ datetime-local, à l'heure du visiteur ; vide tant qu'il ne l'a pas donnée.
  readonly earlier: string;
  readonly direction: CompassPoint | null;
}

// Un signalement complet, ou ce qu'il faut encore demander au visiteur.
export type SightingCheck = { readonly sighting: Sighting } | { readonly problem: string };

function sightingTime({ moment, earlier }: SightingReport, now: Date): Date | null {
  if (moment === "fifteen-minutes-ago") return new Date(now.getTime() - FIFTEEN_MINUTES_MS);
  if (moment === "earlier") return earlier === "" ? null : new Date(earlier);
  return now;
}

export function checkSighting(report: SightingReport, now: Date): SightingCheck {
  if (report.direction === null) return { problem: CHOOSE_DIRECTION };
  const at = sightingTime(report, now);
  if (at === null) return { problem: GIVE_TIME };
  return { sighting: { at, direction: report.direction } };
}
