import { SightingView } from "../templates/SightingView";
import { useAiming } from "../../hooks/useAiming";
import { useSightingReport } from "../../hooks/useSightingReport";
import { COMPASS_ROSE } from "../../lib/compass";
import type { Observer } from "../../lib/observer";

interface SightingPageProps {
  readonly observer: Observer;
  readonly hidden: boolean;
  // Le visiteur dit que la réponse n'était pas la bonne.
  readonly onFeedback: () => void;
}

// « C'était quoi, ça ? » : le visiteur vise ou choisit la direction, puis Là-haut répond.
export function SightingPage({ observer, hidden, onFeedback }: SightingPageProps) {
  const report = useSightingReport(observer);
  const aiming = useAiming({ onPoint: report.choosePoint, onError: report.warn });

  return (
    <SightingView
      hidden={hidden}
      form={{
        moment: report.moment,
        onMoment: report.chooseMoment,
        earlier: report.earlier,
        onEarlier: report.giveEarlier,
        direction: {
          rose: COMPASS_ROSE,
          chosen: report.direction,
          onChoose: (point) => {
            aiming.stop();
            report.choosePoint(point);
          },
          aiming: {
            available: aiming.available,
            active: aiming.active,
            reading: aiming.reading,
            onStart: () => {
              report.dismissAlert();
              void aiming.start();
            },
            onDone: aiming.stop,
          },
        },
        alert: report.alert,
        busy: report.busy,
        onSubmit: () => {
          aiming.stop();
          void report.submit();
        },
      }}
      answer={report.answer}
      onFeedback={onFeedback}
    />
  );
}
