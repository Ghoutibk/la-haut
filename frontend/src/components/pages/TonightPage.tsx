import { TonightView } from "../templates/TonightView";
import { useTonightPasses } from "../../hooks/useTonightPasses";
import type { Observer } from "../../lib/observer";
import { describePass } from "../../lib/tonight";

interface TonightPageProps {
  // Null tant que le navigateur n'a pas situé le visiteur.
  readonly observer: Observer | null;
  readonly hidden: boolean;
}

export function TonightPage({ observer, hidden }: TonightPageProps) {
  const { status, passes } = useTonightPasses(observer);
  const now = new Date();
  return (
    <TonightView
      hidden={hidden}
      status={status}
      passes={passes.map((pass) => describePass(pass, now))}
    />
  );
}
