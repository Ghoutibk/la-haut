import { useEffect, useState } from "react";

import { type VisiblePass, failureMessage, searchPasses } from "../lib/api";
import type { Observer } from "../lib/observer";
import { SEARCHING_PASSES } from "../lib/texts";
import { HOURS_AHEAD, tonightStatus } from "../lib/tonight";

export interface Tonight {
  // Ce que la vue annonce : la recherche en cours, les passages trouvés, ou pourquoi il n'y en a pas.
  readonly status: string;
  readonly passes: readonly VisiblePass[];
}

// Les passages des prochaines heures au-dessus de l'observateur, cherchés dès qu'il est connu.
export function useTonightPasses(observer: Observer | null): Tonight {
  const [tonight, setTonight] = useState<Tonight>({ status: SEARCHING_PASSES, passes: [] });

  useEffect(() => {
    if (observer === null) return;
    let current = true;
    searchPasses(observer, HOURS_AHEAD).then(
      (passes) => {
        if (current) setTonight({ status: tonightStatus(passes), passes });
      },
      (error: unknown) => {
        if (current) setTonight({ status: failureMessage(error), passes: [] });
      },
    );
    return () => {
      current = false;
    };
  }, [observer]);

  return tonight;
}
