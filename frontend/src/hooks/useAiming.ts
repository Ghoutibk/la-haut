import { useEffect, useEffectEvent, useState } from "react";

import { type CompassPoint, aimingAt, compassPointOf, headingFrom } from "../lib/compass";
import { COMPASS_READING } from "../lib/texts";

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
}

export interface Aiming {
  readonly available: boolean;
  readonly active: boolean;
  // Ce que la page dit de la visée : la lecture en cours, puis le point visé.
  readonly reading: string;
  readonly start: () => void;
  readonly stop: () => void;
}

export function useAiming({ onPoint }: AimingCallbacks): Aiming {
  const [available] = useState(canAim);
  const [active, setActive] = useState(false);
  const [reading, setReading] = useState(COMPASS_READING);

  const aimAt = useEffectEvent((point: CompassPoint) => {
    setReading(aimingAt(point));
    onPoint(point);
  });

  useEffect(() => {
    if (!active) return;
    const eventName = orientationEvent();
    function onOrientation(event: Event) {
      const heading = headingFrom(event as DeviceOrientationEvent);
      if (heading !== null) aimAt(compassPointOf(heading));
    }
    window.addEventListener(eventName, onOrientation);
    return () => {
      window.removeEventListener(eventName, onOrientation);
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
