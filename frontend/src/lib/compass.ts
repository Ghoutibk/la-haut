// La boussole du téléphone : de l'événement d'orientation au point cardinal, sans toucher la page.

export const COMPASS_POINTS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"] as const;
export type CompassPoint = (typeof COMPASS_POINTS)[number];

const DEGREES_PER_POINT = 360 / COMPASS_POINTS.length;

export const FRENCH_NAMES: Record<CompassPoint, string> = {
  N: "nord",
  NE: "nord-est",
  E: "est",
  SE: "sud-est",
  S: "sud",
  SW: "sud-ouest",
  W: "ouest",
  NW: "nord-ouest",
};

// Ce qu'un événement d'orientation dit du nord, sur iPhone comme sur Android.
export interface Orientation {
  readonly webkitCompassHeading?: number;
  readonly absolute?: boolean;
  readonly alpha?: number | null;
}

// Le cap vers lequel pointe le haut du téléphone tenu à plat, en degrés depuis le nord dans le
// sens des aiguilles d'une montre ; null si l'appareil ne sait pas où est le nord.
export function headingFrom(orientation: Orientation): number | null {
  const { webkitCompassHeading, absolute, alpha } = orientation;
  // iPhone : la boussole donne le cap directement, ou -1 tant qu'elle n'est pas étalonnée.
  if (typeof webkitCompassHeading === "number") {
    return webkitCompassHeading >= 0 ? webkitCompassHeading % 360 : null;
  }
  // Android : alpha, compté dans le sens inverse, ne vaut que si l'orientation est absolue.
  if (absolute === true && typeof alpha === "number") return (360 - alpha) % 360;
  return null;
}

// Le point cardinal dont le secteur de 45° contient ce cap : le même découpage que le domaine.
export function compassPointOf(heading: number): CompassPoint {
  const index = Math.floor((heading + DEGREES_PER_POINT / 2) / DEGREES_PER_POINT);
  return COMPASS_POINTS[index % COMPASS_POINTS.length] ?? "N";
}
