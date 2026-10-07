import { FRENCH_NAMES, compassPointOf, headingFrom } from "./compass.js";

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
const theDirection = (direction) => (startsWithVowel(direction) ? `l'${direction}` : `le ${direction}`);

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
  result.append(feedbackLink());
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

function feedbackLink() {
  const button = element("button", "link-button", "Ce n'était pas ça ? Dis-le-nous");
  button.type = "button";
  button.addEventListener("click", openFeedback);
  const paragraph = element("p", "hint");
  paragraph.append(button);
  return paragraph;
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

// ---------- Viser avec le téléphone ----------

const COMPASS_PATIENCE_MS = 3000;

// Le téléphone tenu à plat choisit la direction tout seul, en direct, jusqu'à « C'est là ».
// Rend la fonction qui arrête la visée.
function setUpAiming(chooseDirection) {
  const start = $("#aim-start");
  const panel = $("#aiming");
  const reading = $("#aim-reading");
  const error = $("#identify-error");
  const hasCompass = "DeviceOrientationEvent" in window && matchMedia("(pointer: coarse)").matches;
  if (!hasCompass) return () => {};

  start.hidden = false;
  $("#aim-or").hidden = false;
  const eventName = "ondeviceorientationabsolute" in window ? "deviceorientationabsolute" : "deviceorientation";
  let patience;

  function onOrientation(event) {
    const heading = headingFrom(event);
    if (heading === null) return;
    clearTimeout(patience);
    const point = compassPointOf(heading);
    chooseDirection(point);
    reading.textContent = `Tu vises ${theDirection(FRENCH_NAMES[point])}`;
  }

  function stop() {
    window.removeEventListener(eventName, onOrientation);
    clearTimeout(patience);
    panel.hidden = true;
    start.hidden = false;
  }

  start.addEventListener("click", async () => {
    error.textContent = "";
    // L'iPhone demande l'accord de la personne avant de donner la boussole.
    if (typeof DeviceOrientationEvent.requestPermission === "function") {
      const answer = await DeviceOrientationEvent.requestPermission().catch(() => "denied");
      if (answer !== "granted") {
        error.textContent = "Sans accès à la boussole, choisis la direction toi-même.";
        return;
      }
    }
    start.hidden = true;
    panel.hidden = false;
    reading.textContent = "Lecture de la boussole…";
    window.addEventListener(eventName, onOrientation);
    patience = setTimeout(() => {
      stop();
      error.textContent = "La boussole de ton téléphone ne répond pas : choisis la direction toi-même.";
    }, COMPASS_PATIENCE_MS);
  });
  $("#aim-done").addEventListener("click", stop);
  return stop;
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

  const chooseDirection = (point) => {
    sighting.direction = point;
    press(directionButtons, directionButtons.find((button) => button.dataset.direction === point));
    $("#identify-error").textContent = "";
  };
  const stopAiming = setUpAiming(chooseDirection);

  directionButtons.forEach((button) =>
    button.addEventListener("click", () => {
      stopAiming();
      chooseDirection(button.dataset.direction);
    }),
  );

  $("#identify-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    stopAiming();
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

// ---------- Ton avis ----------

const feedback = { kind: "problem" };

async function postJson(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const answer = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(typeof answer.detail === "string" ? answer.detail : "Ton message n'a pas pu partir : vérifie-le et réessaie.");
  }
  return answer;
}

// La fenêtre d'avis s'ouvre toujours sur un formulaire prêt à écrire.
function openFeedback() {
  $("#feedback-result").hidden = true;
  $("#feedback-form").hidden = false;
  $("#feedback-error").textContent = "";
  $("#feedback-dialog").showModal();
}

function setUpFeedback() {
  const dialog = $("#feedback-dialog");
  const form = $("#feedback-form");
  const result = $("#feedback-result");

  $("#feedback-open").addEventListener("click", openFeedback);
  $("#feedback-close").addEventListener("click", () => dialog.close());
  // Un toucher sur le fond assombri ferme aussi la fenêtre. Seul un clic visant la fenêtre
  // elle-même compte : un bouton activé au clavier envoie un clic sans coordonnées.
  dialog.addEventListener("click", (event) => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    const outside =
      event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
    if (outside) dialog.close();
  });
  const kindButtons = [...document.querySelectorAll("[data-kind]")];

  kindButtons.forEach((button) =>
    button.addEventListener("click", () => {
      feedback.kind = button.dataset.kind;
      press(kindButtons, button);
    }),
  );

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const error = $("#feedback-error");
    const message = $("#feedback-message").value.trim();
    if (!message) return void (error.textContent = "Écris ton message avant de l'envoyer.");

    const submit = event.submitter ?? $("#feedback-form .primary");
    submit.setAttribute("aria-busy", "true");
    error.textContent = "";
    try {
      await postJson("/api/feedback", {
        kind: feedback.kind,
        message,
        contact: $("#feedback-contact").value.trim() || null,
        website: $("#feedback-website").value,
      });
      form.reset();
      form.hidden = true;
      result.hidden = false;
    } catch (failure) {
      error.textContent = failure.message;
    } finally {
      submit.removeAttribute("aria-busy");
    }
  });

  $("#feedback-again").addEventListener("click", () => {
    result.hidden = true;
    form.hidden = false;
  });
}

// ---------- Onglets ----------

const VIEWS = { "#ce-soir": "tonight", "#cetait-quoi": "identify" };

function showView() {
  const view = VIEWS[location.hash] ?? "tonight";
  for (const name of Object.values(VIEWS)) $(`#view-${name}`).hidden = view !== name;
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
  setUpFeedback();
  // L'ancienne adresse de l'onglet « Ton avis » ouvre la fenêtre d'avis.
  if (location.hash === "#avis") openFeedback();
  observer = await locateObserver();
  $("#place-label").textContent = observer.label;
  showTonight();
});
