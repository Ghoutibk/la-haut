import { OrbitIcon } from "../atoms/icons";

export function Brand() {
  return (
    <div className="flex items-center gap-2 text-[17px] font-semibold">
      <span className="text-accent">
        <OrbitIcon />
      </span>
      <span>Là-haut</span>
    </div>
  );
}
