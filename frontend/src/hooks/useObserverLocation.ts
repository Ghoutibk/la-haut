import { useEffect, useState } from "react";

import { type Observer, locateObserver } from "../lib/observer";

// L'observateur, une fois que le navigateur a donné sa position ou que la page s'est repliée sur
// Paris ; null jusque-là.
export function useObserverLocation(): Observer | null {
  const [observer, setObserver] = useState<Observer | null>(null);

  useEffect(() => {
    let current = true;
    const source = "geolocation" in navigator ? navigator.geolocation : undefined;
    void locateObserver(source).then((found) => {
      if (current) setObserver(found);
    });
    return () => {
      current = false;
    };
  }, []);

  return observer;
}
