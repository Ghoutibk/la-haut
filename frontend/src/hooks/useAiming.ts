import { useEffect, useEffectEvent, useState } from "react";

import { type CompassPoint, aimingAt, compassPointOf, headingFrom } from "../lib/compass";
import { COMPASS_READING, COMPASS_SILENT } from "../lib/texts";

// Sans cap valide dans ce délai, la boussole est abandonnée.
const COMPASS_PATIENCE_MS = 3000;

// Le téléphone tenu à plat donne la direction : il faut une boussole et un écran tactile.
function canAim(): boolean {
  return "DeviceOrientationEvent" in window && window.matchMedia("(pointer: coarse)").matches;
}

// Chrome sur Android annonce l'orientation absolue par son propre événement, s'il existe.
function orientationEvent(): string {
  return "ondeviceorientationabsolute" in window ? "deviceorientationabsolute" : "deviceorientation";
}

export interface AimingCallbacks {
  // Le point cardinal visé, en direct, à chaque cap lu.
  readonly onPoint: (point: CompassPoint) => void;
  // Ce qui empêche de viser : la page le dit, et le visiteur choisit la direction lui-même.
  readonly onError: (message: string) => void;
}

export interface Aiming {
  readonly available: boolean;
  readonly active: boolean;
  // Ce que la page dit de la visée : la lecture en cours, puis le point visé.
  readonly reading: string;
  readonly start: () => void;
  readonly stop: () => void;
}

export function useAiming({ onPoint, onError }: AimingCallbacks): Aiming {
  const [available] = useState(canAim);
  const [active, setActive] = useState(false);
  const [reading, setReading] = useState(COMPASS_READING);

  const aimAt = useEffectEvent((point: CompassPoint) => {
    setReading(aimingAt(point));
    onPoint(point);
  });
  const giveUp = useEffectEvent(() => {
    setActive(false);
    onError(COMPASS_SILENT);
  });

  useEffect(() => {
    if (!active) return;
    const eventName = orientationEvent();
    const patience = setTimeout(giveUp, COMPASS_PATIENCE_MS);
    function onOrientation(event: Event) {
      const heading = headingFrom(event as DeviceOrientationEvent);
      if (heading === null) return;
      clearTimeout(patience);
      aimAt(compassPointOf(heading));
    }
    window.addEventListener(eventName, onOrientation);
    return () => {
      window.removeEventListener(eventName, onOrientation);
      clearTimeout(patience);
    };
  }, [active]);

  function start() {
    setReading(COMPASS_READING);
    setActive(true);
  }

  function stop() {
    setActive(false);
  }

  return { available, active, reading, start, stop };
}
