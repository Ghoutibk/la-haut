// Une fenêtre posée sur la page : un toucher sur le fond assombri, hors d'elle, la referme.

export interface Box {
  readonly left: number;
  readonly right: number;
  readonly top: number;
  readonly bottom: number;
}

export interface Touch {
  readonly x: number;
  readonly y: number;
}

export function isOutside(box: Box, { x, y }: Touch): boolean {
  return x < box.left || x > box.right || y < box.top || y > box.bottom;
}
