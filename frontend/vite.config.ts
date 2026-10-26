/// <reference types="vitest/config" />
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// La page est servie par FastAPI sous /static, depuis le dossier du paquet Python.
export default defineConfig({
  base: "/static/",
  plugins: [react(), tailwindcss()],
  build: {
    outDir: "../src/la_haut/interface/http/static",
    emptyOutDir: true,
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/testing/setup.ts"],
    // Les heures de la page se lisent à Paris : les tests aussi, quelle que soit la machine.
    env: { TZ: "Europe/Paris" },
  },
});
