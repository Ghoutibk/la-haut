import { type ReactNode, useId } from "react";

import { Eyebrow } from "../atoms/Eyebrow";
import { Title } from "../atoms/Title";

interface ViewSectionProps {
  readonly eyebrow: string;
  // Le titre nomme la vue.
  readonly title: string;
  readonly hidden: boolean;
  readonly children: ReactNode;
}

// Une vue de la page, affichée par son onglet.
export function ViewSection({ eyebrow, title, hidden, children }: ViewSectionProps) {
  const titleId = useId();
  return (
    <section aria-labelledby={titleId} hidden={hidden}>
      <Eyebrow>{eyebrow}</Eyebrow>
      <Title level={1} id={titleId}>
        {title}
      </Title>
      {children}
    </section>
  );
}
