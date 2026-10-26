import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./App";
import "./index.css";

const root = document.getElementById("root");
if (root === null) throw new Error("La page n'a pas d'élément #root où s'afficher.");

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
