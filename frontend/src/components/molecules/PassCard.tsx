import type { PassDescription } from "../../lib/tonight";

export function PassCard({ pass }: { readonly pass: PassDescription }) {
  return (
    <li className="grid grid-cols-[72px_minmax(0,1fr)] items-start gap-3 border-t border-line-soft py-3.5">
      <div className="font-serif text-[28px] leading-none">
        {pass.time}
        {pass.day !== null && (
          <span className="mt-1 block font-sans text-xs text-text-muted">{pass.day}</span>
        )}
      </div>
      <div>
        <div className="font-medium">{pass.name}</div>
        <div className="text-sm text-text-muted">{pass.path}</div>
        <div className="text-sm text-text-soft">{pass.peak}</div>
        {pass.explanation !== null && (
          <div className="text-sm text-text-muted">{pass.explanation}</div>
        )}
      </div>
    </li>
  );
}
