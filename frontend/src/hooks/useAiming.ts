import { useState } from "react";

// Le téléphone tenu à plat donne la direction : il faut une boussole et un écran tactile.
function canAim(): boolean {
  return "DeviceOrientationEvent" in window && window.matchMedia("(pointer: coarse)").matches;
}

export interface Aiming {
  readonly available: boolean;
}

export function useAiming(): Aiming {
  const [available] = useState(canAim);
  return { available };
}
