// Sens des dépendances de la page : la lib ne connaît ni React ni les composants, et chaque niveau
// de l'atomic design n'utilise que les niveaux que la règle lui ouvre.
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const SOURCE = dirname(fileURLToPath(import.meta.url));

const LAYERS = [
  "lib",
  "hooks",
  "atoms",
  "molecules",
  "organisms",
  "templates",
  "pages",
  "app",
] as const;
type Layer = (typeof LAYERS)[number];

// Ce que chaque niveau a le droit d'importer : des modules de ces niveaux, et ces paquets.
const ALLOWED: Record<Layer, { layers: readonly Layer[]; packages: readonly string[] }> = {
  lib: { layers: ["lib"], packages: [] },
  hooks: { layers: ["hooks", "lib"], packages: ["react"] },
  atoms: { layers: ["lib"], packages: ["react"] },
  molecules: { layers: ["atoms"], packages: ["react"] },
  organisms: { layers: ["organisms", "molecules", "atoms"], packages: ["react"] },
  templates: { layers: ["templates", "organisms"], packages: ["react"] },
  pages: { layers: ["templates", "hooks", "lib"], packages: ["react"] },
  // La racine de composition : main.tsx, App.tsx et la feuille de style.
  app: { layers: ["app", "pages", "templates", "hooks", "lib"], packages: ["react", "react-dom"] },
};

// Un type de la lib (CompassPoint, FeedbackKind…) est le vocabulaire de la page : tout niveau peut
// l'importer avec `import type`, qui disparaît à la compilation et n'apporte aucune logique.
const VOCABULARY: Layer = "lib";

interface Import {
  target: string;
  typeOnly: boolean;
}

const IMPORT =
  /\b(?:import|export)\s+(type\s+)?(?:[^'"]*?\s+from\s+)?["']([^"']+)["']|\bimport\s*\(\s*["']([^"']+)["']\s*\)/g;

function sourceFiles(directory: string): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) return entry.name === "testing" ? [] : sourceFiles(path);
    return /\.tsx?$/.test(entry.name) && !/\.test\.tsx?$/.test(entry.name) ? [path] : [];
  });
}

function layerOf(path: string): Layer | "unknown" {
  const [first, second] = relative(SOURCE, path).split(/[\\/]/);
  if (second === undefined) return "app";
  const layer = first === "components" ? second : first;
  return LAYERS.find((known) => known === layer) ?? "unknown";
}

function importsOf(path: string): Import[] {
  return [...readFileSync(path, "utf-8").matchAll(IMPORT)].map((match) => ({
    target: match[2] ?? match[3] ?? "",
    typeOnly: match[1] !== undefined,
  }));
}

function packageOf(target: string): string {
  const [scope, name] = target.split("/");
  return scope?.startsWith("@") ? `${scope}/${name ?? ""}` : (scope ?? target);
}

function isAllowed(path: string, layer: Layer, { target, typeOnly }: Import): boolean {
  const allowed = ALLOWED[layer];
  if (!target.startsWith(".")) return allowed.packages.includes(packageOf(target));
  const targetLayer = layerOf(resolve(dirname(path), target));
  if (targetLayer === "unknown") return false;
  return allowed.layers.includes(targetLayer) || (typeOnly && targetLayer === VOCABULARY);
}

const FILES = sourceFiles(SOURCE);

describe("le sens des dépendances de la page", () => {
  it("range chaque module dans un niveau connu", () => {
    const strays = FILES.filter((path) => layerOf(path) === "unknown");

    expect(strays.map((path) => relative(SOURCE, path))).toEqual([]);
  });

  it.each(LAYERS)("%s n'importe que ce que la règle lui ouvre", (layer) => {
    const violations = FILES.filter((path) => layerOf(path) === layer).flatMap((path) =>
      importsOf(path)
        .filter((found) => !isAllowed(path, layer, found))
        .map(({ target }) => `${relative(SOURCE, path)} → ${target}`),
    );

    expect(violations).toEqual([]);
  });
});
