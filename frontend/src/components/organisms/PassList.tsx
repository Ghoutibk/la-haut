import { Lede } from "../atoms/Lede";
import { PassCard } from "../molecules/PassCard";
import type { PassDescription } from "../../lib/tonight";

interface PassListProps {
  // Ce que la vue annonce : la recherche en cours, les passages trouvés, ou pourquoi il n'y en a pas.
  readonly status: string;
  readonly passes: readonly PassDescription[];
}

export function PassList({ status, passes }: PassListProps) {
  return (
    <>
      <Lede announces>{status}</Lede>
      <ol className="m-0 list-none p-0">
        {passes.map((pass) => (
          <PassCard key={`${pass.day ?? ""} ${pass.time} ${pass.name}`} pass={pass} />
        ))}
      </ol>
    </>
  );
}
