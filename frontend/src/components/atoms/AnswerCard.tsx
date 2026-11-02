import type { ReactNode, Ref } from "react";

interface AnswerCardProps {
  readonly children: ReactNode;
  readonly hidden?: boolean;
  // Pour amener la carte à l'écran quand une réponse y arrive.
  readonly ref?: Ref<HTMLDivElement>;
}

// La carte où arrive une réponse. Elle est en place avant elle, pour que le lecteur d'écran
// l'annonce quand il se tait ; vide, elle ne se voit pas.
export function AnswerCard({ children, hidden = false, ref }: AnswerCardProps) {
  return (
    <div
      ref={ref}
      className="not-empty:mt-6 not-empty:rounded-[20px] not-empty:border not-empty:border-line not-empty:bg-surface not-empty:p-5"
      aria-live="polite"
      hidden={hidden}
    >
      {children}
    </div>
  );
}
