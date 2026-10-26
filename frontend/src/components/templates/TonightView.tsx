import { PassList } from "../organisms/PassList";
import { ViewSection } from "../organisms/ViewSection";
import type { PassDescription } from "../../lib/tonight";

interface TonightViewProps {
  readonly hidden: boolean;
  readonly status: string;
  readonly passes: readonly PassDescription[];
}

export function TonightView({ hidden, status, passes }: TonightViewProps) {
  return (
    <ViewSection eyebrow="Ce soir" title="Au-dessus de toi" hidden={hidden}>
      <PassList status={status} passes={passes} />
    </ViewSection>
  );
}
