// La réponse à « C'était quoi, ça ? » : le candidat le plus probable, les autres, et ce qui n'a pas
// pu être vérifié, en phrases prêtes à lire.

import type { Candidate, Identification, PlanetPosition, VisiblePass } from "./api";
import { fromThe, towardThe } from "./french";
import { PLANET_EXPLANATION, SATELLITES_UNCHECKED, TRAIN_EXPLANATION } from "./texts";
import { clockTime } from "./time";

export interface Answer {
  readonly eyebrow: string;
  readonly title: string;
  readonly sentences: readonly string[];
}

const MOST_LIKELY = "C'était très probablement";
const NOTHING_KNOWN = "Rien de connu";

function passAnswer(best: VisiblePass): Answer {
  const start = clockTime(new Date(best.starts_at));
  const end = clockTime(new Date(best.ends_at));
  const path = `${fromThe(best.appears_in.label)} ${towardThe(best.vanishes_in.label)}`;
  return {
    eyebrow: MOST_LIKELY,
    title: best.name,
    sentences: [
      `Visible de ${start} à ${end}, ${path}.`,
      `Au plus haut à ${String(best.max_elevation_deg)}° au-dessus de l'horizon.`,
      ...(best.kind === "train" ? [TRAIN_EXPLANATION] : []),
    ],
  };
}

function planetAnswer(best: PlanetPosition, satellitesChecked: boolean): Answer {
  const position = `${towardThe(best.direction.label)}, à ${String(best.elevation_deg)}° au-dessus de l'horizon`;
  return {
    eyebrow: satellitesChecked ? MOST_LIKELY : "C'était peut-être",
    title: best.name,
    sentences: [`${best.name} brillait ${position}.`, PLANET_EXPLANATION],
  };
}

function nothingKnown(satellitesChecked: boolean): Answer {
  return satellitesChecked
    ? {
        eyebrow: NOTHING_KNOWN,
        title: "Ni satellite ni planète",
        sentences: [
          "Aucun satellite suivi ni aucune planète brillante n'était dans cette direction à ce moment. C'était peut-être un avion ou une étoile.",
        ],
      }
    : {
        eyebrow: NOTHING_KNOWN,
        title: "Pas une planète",
        sentences: ["Aucune planète brillante n'était dans cette direction à ce moment."],
      };
}

function bestAnswer([best, ...others]: readonly Candidate[], satellitesChecked: boolean): Answer {
  if (best === undefined) return nothingKnown(satellitesChecked);
  const answer = best.kind === "planet" ? planetAnswer(best, satellitesChecked) : passAnswer(best);
  if (others.length === 0) return answer;
  const names = others.map((candidate) => candidate.name).join(", ");
  return { ...answer, sentences: [...answer.sentences, `Ou peut-être : ${names}.`] };
}

export function answerTo({ candidates, satellites_checked }: Identification): Answer {
  const answer = bestAnswer(candidates, satellites_checked);
  if (satellites_checked) return answer;
  return { ...answer, sentences: [...answer.sentences, SATELLITES_UNCHECKED] };
}
