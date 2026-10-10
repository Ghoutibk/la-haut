// Les assertions du DOM (toBeVisible, toHaveAttribute…) pour Vitest, et un DOM vidé après chaque test.
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(cleanup);
