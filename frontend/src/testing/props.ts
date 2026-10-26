// Les props des composants de la page, prêtes pour un test : chacun ne change que ce qu'il vérifie.

import { vi } from "vitest";

import type { FeedbackDialogProps } from "../components/organisms/FeedbackDialog";
import type { FeedbackFormProps } from "../components/organisms/FeedbackForm";
import type { AimingProps, DirectionPickerProps } from "../components/organisms/DirectionPicker";
import type { SightingFormProps } from "../components/organisms/SightingForm";
import { COMPASS_ROSE } from "../lib/compass";
import type { FeedbackDraft } from "../lib/feedback";

export const A_DRAFT: FeedbackDraft = { kind: "problem", message: "", contact: "", website: "" };

export function anAiming(changes: Partial<AimingProps> = {}): AimingProps {
  return {
    available: false,
    active: false,
    reading: "Lecture de la boussole…",
    onStart: vi.fn(),
    onDone: vi.fn(),
    ...changes,
  };
}

export function aDirectionPicker(
  changes: Partial<DirectionPickerProps> = {},
): DirectionPickerProps {
  return { rose: COMPASS_ROSE, chosen: null, onChoose: vi.fn(), aiming: anAiming(), ...changes };
}

export function aSightingForm(changes: Partial<SightingFormProps> = {}): SightingFormProps {
  return {
    moment: "now",
    onMoment: vi.fn(),
    earlier: "",
    onEarlier: vi.fn(),
    direction: aDirectionPicker(),
    alert: "",
    busy: false,
    onSubmit: vi.fn(),
    ...changes,
  };
}

export function aFeedbackForm(changes: Partial<FeedbackFormProps> = {}): FeedbackFormProps {
  return {
    draft: A_DRAFT,
    onRevise: vi.fn(),
    alert: "",
    busy: false,
    onSend: vi.fn(),
    hidden: false,
    ...changes,
  };
}

export function aFeedbackDialog(changes: Partial<FeedbackDialogProps> = {}): FeedbackDialogProps {
  return {
    open: true,
    onClose: vi.fn(),
    thanked: false,
    onWriteAnother: vi.fn(),
    form: aFeedbackForm(),
    ...changes,
  };
}
