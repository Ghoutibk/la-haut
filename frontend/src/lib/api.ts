// L'API HTTP de Là-haut, telle que la page l'appelle. Les types suivent le JSON des présentateurs.

import type { CompassPoint } from "./compass";
import type { Observer } from "./observer";
import { MESSAGE_NOT_SENT, SKY_UNREACHABLE } from "./texts";

export interface Direction {
  readonly code: CompassPoint;
  readonly label: string;
}

export interface VisiblePass {
  readonly kind: "satellite" | "train";
  readonly name: string;
  readonly starts_at: string;
  readonly ends_at: string;
  readonly duration_s: number;
  readonly appears_in: Direction;
  readonly vanishes_in: Direction;
  readonly max_elevation_deg: number;
}

export interface PlanetPosition {
  readonly kind: "planet";
  readonly name: string;
  readonly direction: Direction;
  readonly elevation_deg: number;
}

export type Candidate = VisiblePass | PlanetPosition;

export interface Identification {
  readonly candidates: readonly Candidate[];
  readonly satellites_checked: boolean;
}

export interface Sighting {
  readonly at: Date;
  readonly direction: CompassPoint;
}

export type FeedbackKind = "problem" | "idea" | "other";

// Le formulaire « Ton avis », tel que l'API le reçoit.
export interface FeedbackForm {
  readonly kind: FeedbackKind;
  readonly message: string;
  readonly contact: string | null;
  readonly website: string;
}

function detailOf(body: unknown): string | undefined {
  if (typeof body !== "object" || body === null || !("detail" in body)) return undefined;
  return typeof body.detail === "string" ? body.detail : undefined;
}

// Le corps de la réponse ; en cas de refus, l'explication de l'API ou, à défaut, `fallback`.
async function answerOf(response: Response, fallback: string): Promise<unknown> {
  const body: unknown = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(detailOf(body) ?? fallback);
  return body;
}

async function getJson(path: string, params: Record<string, string>): Promise<unknown> {
  const response = await fetch(`${path}?${new URLSearchParams(params).toString()}`);
  return answerOf(response, SKY_UNREACHABLE);
}

function whereIs(observer: Observer): Record<string, string> {
  return { latitude: String(observer.latitude), longitude: String(observer.longitude) };
}

export async function searchPasses(observer: Observer, hours: number): Promise<VisiblePass[]> {
  const answer = (await getJson("/api/passes", { ...whereIs(observer), hours: String(hours) })) as {
    passes: VisiblePass[];
  };
  return answer.passes;
}

export async function identify(observer: Observer, sighting: Sighting): Promise<Identification> {
  return (await getJson("/api/identification", {
    ...whereIs(observer),
    at: sighting.at.toISOString(),
    direction: sighting.direction,
  })) as Identification;
}

export async function sendFeedback(feedback: FeedbackForm): Promise<void> {
  const response = await fetch("/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(feedback),
  });
  await answerOf(response, MESSAGE_NOT_SENT);
}
