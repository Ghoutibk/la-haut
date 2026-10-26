// Les icônes de la page, tracées au trait dans la couleur du texte : décoratives, le lecteur
// d'écran les ignore.

import type { ReactNode } from "react";

interface IconProps {
  readonly size: number;
  readonly strokeWidth: number;
  readonly children: ReactNode;
}

function Icon({ size, strokeWidth, children }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  );
}

export function OrbitIcon() {
  return (
    <Icon size={22} strokeWidth={1.6}>
      <circle cx="12" cy="12" r="3" />
      <ellipse cx="12" cy="12" rx="10" ry="4.5" transform="rotate(-20 12 12)" />
    </Icon>
  );
}

export function PinIcon() {
  return (
    <Icon size={14} strokeWidth={1.8}>
      <path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z" />
      <circle cx="12" cy="9.5" r="2.5" />
    </Icon>
  );
}

export function SpeechBubbleIcon() {
  return (
    <Icon size={14} strokeWidth={1.8}>
      <path d="M20 12a8 8 0 0 1-11.6 7.1L4 20l1-4.1A8 8 0 1 1 20 12z" />
    </Icon>
  );
}

export function CompassIcon() {
  return (
    <Icon size={20} strokeWidth={1.8}>
      <circle cx="12" cy="12" r="9" />
      <path d="M15.5 8.5l-2 5-5 2 2-5z" />
    </Icon>
  );
}

export function MoonIcon() {
  return (
    <Icon size={22} strokeWidth={1.7}>
      <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" />
    </Icon>
  );
}

export function TargetIcon() {
  return (
    <Icon size={22} strokeWidth={1.7}>
      <circle cx="12" cy="12" r="8" />
      <circle cx="12" cy="12" r="2" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
    </Icon>
  );
}
