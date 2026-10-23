// L'heure et le jour tels que le visiteur les lit, dans son fuseau.

const CLOCK = new Intl.DateTimeFormat("fr-FR", { hour: "2-digit", minute: "2-digit" });
const DAY = new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long" });
const SECONDS_PER_MINUTE = 60;

export function clockTime(instant: Date): string {
  return CLOCK.format(instant);
}

export function dayName(instant: Date): string {
  return DAY.format(instant);
}

export function isSameDay(instant: Date, other: Date): boolean {
  return instant.toDateString() === other.toDateString();
}

export function minutesOf(seconds: number): number {
  return Math.max(1, Math.round(seconds / SECONDS_PER_MINUTE));
}
