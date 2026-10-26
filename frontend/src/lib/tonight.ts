// La vue « Ce soir » : ce qu'elle annonce, et chaque passage tel que le visiteur le lit.

import type { VisiblePass } from "./api";
import { TRAIN_EXPLANATION } from "./texts";
import { clockTime, dayName, isSameDay, minutesOf } from "./time";

export const HOURS_AHEAD = 12;

export interface PassDescription {
  readonly time: string;
  // Le jour, seulement si le passage n'a pas lieu aujourd'hui.
  readonly day: string | null;
  readonly name: string;
  readonly path: string;
  readonly peak: string;
  readonly explanation: string | null;
}

export function tonightStatus(passes: readonly VisiblePass[]): string {
  return passes.length > 0
    ? `Les satellites célèbres et les trains Starlink visibles à l'œil nu dans les ${String(HOURS_AHEAD)} prochaines heures.`
    : `Aucun passage visible dans les ${String(HOURS_AHEAD)} prochaines heures. Les satellites se voient surtout peu après le coucher du soleil et avant l'aube.`;
}

export function describePass(pass: VisiblePass, now: Date): PassDescription {
  const start = new Date(pass.starts_at);
  return {
    time: clockTime(start),
    day: isSameDay(start, now) ? null : dayName(start),
    name: pass.name,
    path: `${pass.appears_in.label} → ${pass.vanishes_in.label} · ${String(minutesOf(pass.duration_s))} min`,
    peak: `Au plus haut à ${String(pass.max_elevation_deg)}° au-dessus de l'horizon`,
    explanation: pass.kind === "train" ? TRAIN_EXPLANATION : null,
  };
}
