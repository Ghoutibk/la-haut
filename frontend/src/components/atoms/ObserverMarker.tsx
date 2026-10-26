// La case du milieu de la rose des vents : le visiteur, d'où partent les directions.
export function ObserverMarker() {
  return (
    <span
      className="flex items-center justify-center gap-1.5 text-[13px] text-text-muted"
      aria-hidden="true"
    >
      <i className="size-2 rounded-full bg-sky-blue" />
      Toi
    </span>
  );
}
