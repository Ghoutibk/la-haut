"use strict";

const PARIS = { latitude: 48.8566, longitude: 2.3522, label: "Paris" };
const FIFTEEN_MINUTES_MS = 15 * 60 * 1000;
const timeFormat = new Intl.DateTimeFormat("fr-FR", { hour: "2-digit", minute: "2-digit" });
const dayFormat = new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long" });

const $ = (selector) => document.querySelector(selector);
let observer = PARIS;

// ---------- Position de l'observateur ----------

function roundCoordinate(value) {
  return Math.round(value * 100) / 100; // ~1 km : assez précis pour le ciel, pas plus
}

const LOCATION_PATIENCE_MS = 6000;

function locateObserver() {
  return new Promise((resolve) => {
    if (!("geolocation" in navigator)) return resolve(PARIS);
    // Sans réponse à la demande d'autorisation, on n'attend pas indéfiniment.
    setTimeout(() => resolve(PARIS), LOCATION_PATIENCE_MS);
    navigator.geolocation.getCurrentPosition(
      ({ coords }) =>
        resolve({
          latitude: roundCoordinate(coords.latitude),
          longitude: roundCoordinate(coords.longitude),
          label: "Ta position",
        }),
      () => resolve(PARIS),
      { maximumAge: 10 * 60 * 1000, timeout: 8000 },
    );
  });
}

// ---------- Appels à l'API ----------

async function getJson(path, params) {
  const query = new URLSearchParams({
    latitude: observer.latitude,
    longitude: observer.longitude,
    ...params,
  });
  const response = await fetch(`${path}?${query}`);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(typeof body.detail === "string" ? body.detail : "Le ciel est injoignable pour le moment.");
  }
  return body;
}

// ---------- Rendu ----------

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function minutesBetween(start, end) {
  return Math.max(1, Math.round((new Date(end) - new Date(start)) / 60000));
}

function route(pass) {
  return `${pass.appears_in.label} → ${pass.vanishes_in.label} · ${minutesBetween(pass.starts_at, pass.ends_at)} min`;
}

const startsWithVowel = (word) => /^[aeiouy]/i.test(word);
const fromThe = (direction) => (startsWithVowel(direction) ? `de l'${direction}` : `du ${direction}`);
const towardThe = (direction) => (startsWithVowel(direction) ? `vers l'${direction}` : `vers le ${direction}`);

function isToday(date) {
  return date.toDateString() === new Date().toDateString();
}

const TRAIN_EXPLANATION =
  "Une file de points brillants qui se suivent : les satellites Starlink d'un même lancement, quelques jours après leur mise en orbite.";

const PLANET_EXPLANATION =
  "Une planète ne bouge pas en quelques minutes : elle reste au même endroit parmi les étoiles. Si ta lumière filait dans le ciel, c'était plutôt un satellite ou un avion.";

const SATELLITES_UNCHECKED =
  "Le catalogue des satellites est indisponible pour le moment : seules les planètes ont été vérifiées. Réessaie plus tard pour savoir si c'était un satellite.";

function renderPass(pass) {
  const start = new Date(pass.starts_at);
  const item = element("li", "pass");

  const time = element("div", "pass-time", timeFormat.format(start));
  if (!isToday(start)) time.append(element("span", "pass-day", dayFormat.format(start)));

  const details = element("div");
  details.append(
    element("div", "pass-name", pass.name),
    element("div", "pass-meta", route(pass)),
    element("div", "pass-extra", `Au plus haut à ${pass.max_elevation_deg}° au-dessus de l'horizon`),
  );
  if (pass.kind === "train") details.append(element("div", "pass-meta", TRAIN_EXPLANATION));

  item.append(time, details);
  return item;
}

async function showTonight() {
  const status = $("#tonight-status");
  const list = $("#passes");
  status.textContent = "Recherche des passages…";
  list.replaceChildren();
  try {
    const { passes } = await getJson("/api/passes", { hours: 12 });
    status.textContent = passes.length
      ? "Les satellites célèbres et les trains Starlink visibles à l'œil nu dans les 12 prochaines heures."
      : "Aucun passage visible dans les 12 prochaines heures. Les satellites se voient surtout peu après le coucher du soleil et avant l'aube.";
    list.append(...passes.map(renderPass));
  } catch (error) {
    status.textContent = error.message;
  }
}

function renderIdentification({ candidates, satellites_checked: satellitesChecked }) {
  const result = $("#identify-result");
  if (candidates.length) {
    renderCandidates(result, candidates, satellitesChecked);
  } else if (satellitesChecked) {
    result.replaceChildren(
      element("p", "eyebrow", "Rien de connu"),
      element("h2", null, "Ni satellite ni planète"),
      element("p", null, "Aucun satellite suivi ni aucune planète brillante n'était dans cette direction à ce moment. C'était peut-être un avion ou une étoile."),
    );
  } else {
    result.replaceChildren(
      element("p", "eyebrow", "Rien de connu"),
      element("h2", null, "Pas une planète"),
      element("p", null, "Aucune planète brillante n'était dans cette direction à ce moment."),
    );
  }
  if (!satellitesChecked) result.append(element("p", null, SATELLITES_UNCHECKED));
}

function renderCandidates(result, candidates, satellitesChecked) {
  const [best, ...others] = candidates;
  if (best.kind === "planet") {
    result.replaceChildren(
      element("p", "eyebrow", satellitesChecked ? "C'était très probablement" : "C'était peut-être"),
      element("h2", null, best.name),
      element("p", null, `${best.name} brillait ${towardThe(best.direction.label)}, à ${best.elevation_deg}° au-dessus de l'horizon.`),
      element("p", null, PLANET_EXPLANATION),
    );
  } else {
    renderPassIdentification(result, best);
  }
  if (others.length) {
    result.append(element("p", null, `Ou peut-être : ${others.map((candidate) => candidate.name).join(", ")}.`));
  }
}

function renderPassIdentification(result, best) {
  const start = new Date(best.starts_at);
  const end = new Date(best.ends_at);
  result.replaceChildren(
    element("p", "eyebrow", "C'était très probablement"),
    element("h2", null, best.name),
    element("p", null, `Visible de ${timeFormat.format(start)} à ${timeFormat.format(end)}, ${fromThe(best.appears_in.label)} ${towardThe(best.vanishes_in.label)}.`),
    element("p", null, `Au plus haut à ${best.max_elevation_deg}° au-dessus de l'horizon.`),
  );
  if (best.kind === "train") result.append(element("p", null, TRAIN_EXPLANATION));
}

// ---------- Formulaire « C'était quoi, ça ? » ----------

const sighting = { when: "now", direction: null };

function press(buttons, chosen) {
  buttons.forEach((button) => button.setAttribute("aria-pressed", String(button === chosen)));
}

function sightingTime() {
  if (sighting.when === "15") return new Date(Date.now() - FIFTEEN_MINUTES_MS);
  if (sighting.when === "earlier") {
    const value = $("#earlier-input").value;
    return value ? new Date(value) : null;
  }
  return new Date();
}

function setUpIdentification() {
  const whenButtons = [...document.querySelectorAll("[data-when]")];
  const directionButtons = [...document.querySelectorAll("[data-direction]")];

  whenButtons.forEach((button) =>
    button.addEventListener("click", () => {
      sighting.when = button.dataset.when;
      press(whenButtons, button);
      $("#earlier-field").hidden = sighting.when !== "earlier";
    }),
  );

  directionButtons.forEach((button) =>
    button.addEventListener("click", () => {
      sighting.direction = button.dataset.direction;
      press(directionButtons, button);
      $("#identify-error").textContent = "";
    }),
  );

  $("#identify-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const error = $("#identify-error");
    const at = sightingTime();
    if (!sighting.direction) return void (error.textContent = "Choisis la direction où tu l'as vue.");
    if (!at) return void (error.textContent = "Indique l'heure à laquelle tu l'as vue.");

    const submit = event.submitter ?? $("#identify-form .primary");
    submit.setAttribute("aria-busy", "true");
    error.textContent = "";
    try {
      const identification = await getJson("/api/identification", {
        at: at.toISOString(),
        direction: sighting.direction,
      });
      renderIdentification(identification);
    } catch (failure) {
      error.textContent = failure.message;
    } finally {
      submit.removeAttribute("aria-busy");
    }
  });
}

// ---------- Onglets ----------

const VIEWS = { "#ce-soir": "tonight", "#cetait-quoi": "identify" };

function showView() {
  const view = VIEWS[location.hash] ?? "tonight";
  $("#view-tonight").hidden = view !== "tonight";
  $("#view-identify").hidden = view !== "identify";
  document.querySelectorAll(".tab").forEach((tab) => {
    if (tab.dataset.view === view) tab.setAttribute("aria-current", "page");
    else tab.removeAttribute("aria-current");
  });
}

// ---------- Démarrage ----------

window.addEventListener("hashchange", showView);
document.addEventListener("DOMContentLoaded", async () => {
  showView();
  setUpIdentification();
  observer = await locateObserver();
  $("#place-label").textContent = observer.label;
  showTonight();
});
