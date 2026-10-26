import { type ReactNode, useEffect, useRef } from "react";

import { isOutside } from "../../lib/dialog";

interface SheetProps {
  readonly open: boolean;
  // Le navigateur l'a fermée : par Échap, ou d'un toucher sur le fond assombri.
  readonly onClose: () => void;
  // L'identifiant du titre qui la nomme.
  readonly labelledBy: string;
  readonly children: ReactNode;
}

// La fenêtre qui monte du bas de l'écran, comme une feuille sur un téléphone.
export function Sheet({ open, onClose, labelledBy, children }: SheetProps) {
  const dialog = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const sheet = dialog.current;
    if (sheet === null || sheet.open === open) return;
    if (open) sheet.showModal();
    else sheet.close();
  }, [open]);

  return (
    <dialog
      ref={dialog}
      className="mx-auto mt-auto mb-0 max-h-[92dvh] w-full max-w-120 overflow-y-auto rounded-t-[22px] border border-b-0 border-line bg-night px-4 pt-4.5 pb-[max(20px,env(safe-area-inset-bottom))] text-text backdrop:bg-black/60"
      aria-labelledby={labelledBy}
      onClose={onClose}
      onClick={(event) => {
        // Seul un toucher visant la fenêtre elle-même compte : un bouton activé au clavier, lui,
        // envoie un clic sans coordonnées à ce bouton.
        if (event.target !== event.currentTarget) return;
        const touch = { x: event.clientX, y: event.clientY };
        if (isOutside(event.currentTarget.getBoundingClientRect(), touch)) onClose();
      }}
    >
      {children}
    </dialog>
  );
}
