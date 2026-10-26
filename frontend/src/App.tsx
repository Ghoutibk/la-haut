import { SightingPage } from "./components/pages/SightingPage";
import { TonightPage } from "./components/pages/TonightPage";
import { MobileShell } from "./components/templates/MobileShell";
import { useFeedback } from "./hooks/useFeedback";
import { useHashView } from "./hooks/useHashView";
import { useObserverLocation } from "./hooks/useObserverLocation";
import { PARIS } from "./lib/observer";
import { VIEW_ANCHORS, opensFeedback } from "./lib/route";

// La page de Là-haut : la vue de l'ancre, le lieu du visiteur et la fenêtre d'avis.
export function App() {
  const view = useHashView();
  const observer = useObserverLocation();
  // L'ancienne adresse de l'onglet « Ton avis » ouvre la fenêtre, au chargement seulement.
  const feedback = useFeedback(opensFeedback(window.location.hash));
  // Tant que le navigateur n'a pas situé le visiteur, Là-haut regarde depuis Paris.
  const place = observer ?? PARIS;

  return (
    <MobileShell
      topBar={{ place: place.label, onFeedback: feedback.open }}
      tabBar={{ anchors: VIEW_ANCHORS, current: view }}
      feedback={{
        open: feedback.isOpen,
        onClose: feedback.close,
        thanked: feedback.thanked,
        onWriteAnother: feedback.writeAnother,
        form: {
          draft: feedback.draft,
          onRevise: feedback.revise,
          alert: feedback.alert,
          busy: feedback.busy,
          onSend: () => {
            void feedback.send();
          },
        },
      }}
    >
      <TonightPage observer={observer} hidden={view !== "tonight"} />
      <SightingPage observer={place} hidden={view !== "sighting"} onFeedback={feedback.open} />
    </MobileShell>
  );
}
