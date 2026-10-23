// Là d'où le visiteur regarde le ciel : sa position s'il la donne, Paris sinon.

export interface Observer {
  readonly latitude: number;
  readonly longitude: number;
  readonly label: string;
}

export const PARIS: Observer = { latitude: 48.8566, longitude: 2.3522, label: "Paris" };

// Sans réponse à la demande d'autorisation, la page n'attend pas indéfiniment.
const LOCATION_PATIENCE_MS = 6000;
const LOCATION_OPTIONS = { maximumAge: 10 * 60 * 1000, timeout: 8000 };

// Ce que la page attend de la géolocalisation du navigateur.
export interface PositionSource {
  getCurrentPosition(
    found: (position: { coords: { latitude: number; longitude: number } }) => void,
    failed: () => void,
    options: typeof LOCATION_OPTIONS,
  ): void;
}

// Environ 1 km : assez précis pour le ciel, pas plus.
function roundCoordinate(value: number): number {
  return Math.round(value * 100) / 100;
}

export function locateObserver(source: PositionSource | undefined): Promise<Observer> {
  return new Promise((resolve) => {
    if (source === undefined) {
      resolve(PARIS);
      return;
    }
    setTimeout(() => {
      resolve(PARIS);
    }, LOCATION_PATIENCE_MS);
    source.getCurrentPosition(
      ({ coords }) => {
        resolve({
          latitude: roundCoordinate(coords.latitude),
          longitude: roundCoordinate(coords.longitude),
          label: "Ta position",
        });
      },
      () => {
        resolve(PARIS);
      },
      LOCATION_OPTIONS,
    );
  });
}
