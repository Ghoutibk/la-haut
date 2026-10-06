// La boussole du téléphone : de l'événement d'orientation au point cardinal, sans toucher la page.

export const COMPASS_POINTS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
const DEGREES_PER_POINT = 360 / COMPASS_POINTS.length;

export const FRENCH_NAMES = {
  N: "nord",
  NE: "nord-est",
  E: "est",
  SE: "sud-est",
  S: "sud",
  SW: "sud-ouest",
  W: "ouest",
  NW: "nord-ouest",
};

// Le cap vers lequel pointe le haut du téléphone tenu à plat, en degrés depuis le nord dans le
// sens des aiguilles d'une montre ; null si l'appareil ne sait pas où est le nord.
export function headingFrom(event) {
  // iPhone : la boussole donne le cap directement, ou -1 tant qu'elle n'est pas étalonnée.
  if (typeof event.webkitCompassHeading === "number") {
    return event.webkitCompassHeading >= 0 ? event.webkitCompassHeading % 360 : null;
  }
  // Android : alpha, compté dans le sens inverse, ne vaut que si l'orientation est absolue.
  if (event.absolute && typeof event.alpha === "number") return (360 - event.alpha) % 360;
  return null;
}

// Le point cardinal dont le secteur de 45° contient ce cap : le même découpage que le domaine.
export function compassPointOf(heading) {
  const index = Math.floor((heading + DEGREES_PER_POINT / 2) / DEGREES_PER_POINT);
  return COMPASS_POINTS[index % COMPASS_POINTS.length];
}
