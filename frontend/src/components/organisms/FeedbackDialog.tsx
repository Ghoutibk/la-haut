import { useId } from "react";

import { Lede } from "../atoms/Lede";
import { Sheet } from "../atoms/Sheet";
import { Title } from "../atoms/Title";
import { FeedbackThanks } from "../molecules/FeedbackThanks";
import { SheetHeader } from "../molecules/SheetHeader";
import { FeedbackForm, type FeedbackFormProps } from "./FeedbackForm";

export interface FeedbackDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  // Le message est arrivé : la fenêtre remercie au lieu de montrer le formulaire.
  readonly thanked: boolean;
  readonly onWriteAnother: () => void;
  readonly form: Omit<FeedbackFormProps, "hidden">;
}

// « Un souci, une idée ? » : la fenêtre d'avis, ouverte par-dessus n'importe quelle vue.
export function FeedbackDialog({
  open,
  onClose,
  thanked,
  onWriteAnother,
  form,
}: FeedbackDialogProps) {
  const titleId = useId();
  return (
    <Sheet open={open} onClose={onClose} labelledBy={titleId}>
      <SheetHeader eyebrow="Ton avis" onClose={onClose} />
      <Title level={2} id={titleId}>
        Un souci, une idée ?
      </Title>
      <Lede>
        Dis-nous ce qui ne marche pas ou ce qui te manquerait. Ton message n'est lu que par l'auteur
        du site.
      </Lede>
      <FeedbackForm {...form} hidden={thanked} />
      <FeedbackThanks hidden={!thanked} onWriteAnother={onWriteAnother} />
    </Sheet>
  );
}
