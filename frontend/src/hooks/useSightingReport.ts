import { useState } from "react";

import { failureMessage, identify } from "../lib/api";
import type { CompassPoint } from "../lib/compass";
import { type Answer, answerTo } from "../lib/identification";
import type { Observer } from "../lib/observer";
import { type SightingMoment, checkSighting } from "../lib/sighting";

export interface SightingReportForm {
  readonly moment: SightingMoment;
  readonly chooseMoment: (moment: SightingMoment) => void;
  // L'heure donnée « Plus tôt », telle que le champ datetime-local la tient.
  readonly earlier: string;
  readonly giveEarlier: (earlier: string) => void;
  readonly direction: CompassPoint | null;
  readonly choosePoint: (point: CompassPoint) => void;
  // Ce que la vue signale au visiteur : un signalement incomplet, un refus de Là-haut, ou ce qui
  // empêche de viser ; vide sinon.
  readonly alert: string;
  readonly warn: (message: string) => void;
  readonly dismissAlert: () => void;
  readonly busy: boolean;
  readonly answer: Answer | null;
  readonly submit: () => Promise<void>;
}

// « C'était quoi, ça ? » : ce que le visiteur remplit, puis la réponse de Là-haut.
export function useSightingReport(observer: Observer): SightingReportForm {
  const [moment, setMoment] = useState<SightingMoment>("now");
  const [earlier, setEarlier] = useState("");
  const [direction, setDirection] = useState<CompassPoint | null>(null);
  const [alert, setAlert] = useState("");
  const [busy, setBusy] = useState(false);
  const [answer, setAnswer] = useState<Answer | null>(null);

  function choosePoint(point: CompassPoint) {
    setDirection(point);
    setAlert("");
  }

  async function submit() {
    const check = checkSighting({ moment, earlier, direction }, new Date());
    if ("problem" in check) {
      setAlert(check.problem);
      return;
    }
    setAlert("");
    setBusy(true);
    try {
      setAnswer(answerTo(await identify(observer, check.sighting)));
    } catch (error) {
      setAlert(failureMessage(error));
    } finally {
      setBusy(false);
    }
  }

  return {
    moment,
    chooseMoment: setMoment,
    earlier,
    giveEarlier: setEarlier,
    direction,
    choosePoint,
    alert,
    warn: setAlert,
    dismissAlert: () => {
      setAlert("");
    },
    busy,
    answer,
    submit,
  };
}
