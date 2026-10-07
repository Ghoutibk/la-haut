# Là-haut

Ce qui passe au-dessus de toi ce soir : les satellites visibles à l'œil nu depuis chez toi, et la réponse à « c'était quoi, cette lumière ? ».

## Ce que fait Là-haut aujourd'hui

Pour un observateur et une période, Là-haut liste les passages visibles à l'œil nu des satellites célèbres (l'ISS, Tiangong et Hubble) et des trains Starlink. Les éléments orbitaux viennent de deux groupes CelesTrak, téléchargés au besoin et gardés deux heures en cache chacun : « visual » pour les satellites célèbres, « last-30-days » pour les Starlink lancés dans les 30 derniers jours. Ils sont téléchargés au format OMM, en CSV : depuis mi-2026, les objets nouvellement lancés reçoivent des numéros NORAD au-delà de 99999, que le format TLE ne sait pas écrire, et CelesTrak ne publie plus les lancements récents qu'en OMM. Si un groupe est injoignable et sans cache, l'autre continue d'être annoncé. Après un téléchargement raté, CelesTrak n'est pas redemandé avant 15 minutes : les visites suivantes répondent tout de suite, avec le dernier catalogue connu s'il existe. Chaque échec est écrit dans les logs avec sa cause. Le calcul des passages tourne hors ligne : propagation SGP4 et position du Soleil avec Skyfield, éphémérides DE421 embarquées. Un balayage toutes les minutes trouve quand chaque satellite est au-dessus de l'horizon ; seuls ces moments sont échantillonnés toutes les 10 secondes. « Ce soir » se calcule par quarts d'heure : les visites d'un même observateur dans le même quart d'heure reçoivent les passages déjà calculés. Les objets amarrés ensemble sont annoncés comme un seul passage. Les Starlink d'un même lancement qui défilent en file sur le même chemin le sont aussi, sous le nom « Train Starlink (N satellites) » : c'est la file de points que l'on prend pour des OVNI.

À partir d'un signalement (« j'ai vu une lumière à telle heure, direction sud-est »), Là-haut retrouve aussi ce qui était là : c'est « C'était quoi, ça ? ». Il cherche d'abord parmi les satellites suivis, trains Starlink compris, puis parmi les planètes brillantes que l'on prend souvent pour un satellite ou un avion : Vénus, Jupiter, Mars et Saturne. Une planète est candidate si elle était au-dessus de l'horizon, dans un ciel assez sombre (Soleil à −6° ou moins), dans la direction indiquée ou une direction voisine ; les planètes sont classées de la plus proche à la plus éloignée de cette direction, après les satellites. Leurs positions sont calculées hors ligne avec les éphémérides DE421 embarquées : sans aucun catalogue de satellites, les planètes répondent quand même, et la réponse précise que les satellites n'ont pas pu être vérifiés.

Les deux sont accessibles sur un site web : une page mobile avec les onglets « Ce soir » et « C'était quoi ? », appuyée sur une API HTTP. Le bouton « Avis » de l'en-tête, comme le lien « Ce n'était pas ça ? Dis-le-nous » sous chaque identification, ouvre une fenêtre pour signaler un problème ou proposer une idée, avec un e-mail facultatif pour recevoir une réponse ; chaque message devient un ticket du dépôt privé `Ghoutibk/la-haut-avis`. Pour dire où la lumière était, inutile de connaître les points cardinaux : sur un téléphone, « Viser avec mon téléphone » lit la boussole. On tient le téléphone à plat, le haut de l'écran vers l'endroit où on a vu la lumière, et la direction se choisit en direct jusqu'à « C'est là ». L'iPhone demande d'abord l'autorisation. Sans boussole, ou sur un ordinateur, on choisit parmi huit boutons, avec un repère : le Soleil se lève vers l'est et se couche vers l'ouest.

## Démarrer

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

## Lancer le site

```bash
uvicorn --factory la_haut.composition:build_web_app --reload
```

Puis ouvre http://127.0.0.1:8000. La page demande ta position et se replie sur Paris si tu refuses ou ne réponds pas. Le cache CelesTrak se trouve dans `~/.cache/la-haut/visual.csv`, à côté de `last-30-days.csv` ; la variable d'environnement `LA_HAUT_CACHE` permet de déplacer les deux. `LA_HAUT_CATALOG_URL` change la source des catalogues : une adresse où `{group}` est remplacé par le nom du groupe, CelesTrak par défaut.

| Route | Rôle |
|---|---|
| `GET /` | La page web |
| `GET /health` | Vérification de santé pour l'hébergeur : répond 200 sans rien calculer |
| `GET /api/passes?latitude=&longitude=&hours=12` | Les passages visibles des prochaines heures (1 à 48) |
| `GET /api/identification?latitude=&longitude=&at=&direction=` | « C'était quoi, ça ? » : `at` en ISO 8601 avec fuseau, `direction` parmi N, NE, E, SE, S, SW, W, NW. Chaque candidat porte un `kind` : `satellite`, `train` ou `planet`. `satellites_checked` vaut `false` quand le catalogue des satellites manquait et que seules les planètes ont été cherchées |
| `POST /api/feedback` | Un avis en JSON : `kind` parmi `problem`, `idea`, `other`, `message` (2 000 caractères au plus), `contact` facultatif. Répond 201, 422 avec une raison lisible, 429 au-delà de 20 avis par heure, ou 503 si la boîte à avis est indisponible |

## Lancer l'image Docker

```bash
docker build -t la-haut .
docker run --rm -p 8000:8000 la-haut
```

L'image (Python 3.13 slim) tourne sous un utilisateur non root, écoute sur le port donné par `$PORT` (8000 par défaut) et garde ses catalogues CelesTrak dans `/tmp/la-haut`.

## Mettre en ligne

Le dépôt contient une blueprint Render (`render.yaml`) : un service web gratuit, construit depuis le `Dockerfile`, région Francfort, surveillé sur `/health`. Le déploiement se fait depuis le compte du propriétaire du dépôt :

1. Crée un compte sur [render.com](https://render.com), de préférence en te connectant avec GitHub.
2. Dans le tableau de bord, choisis **New** → **Blueprint**.
3. Relie ton compte GitHub si Render le demande, et autorise l'accès au dépôt `la-haut` (tous les dépôts ou seulement celui-ci).
4. Choisis le dépôt `la-haut` et la branche `main` : Render lit `render.yaml` et propose le service `la-haut` sur l'offre **Free**. Valide avec **Apply**.
5. Attends la fin de la construction de l'image (quelques minutes), puis ouvre l'adresse donnée par Render, du type `https://la-haut.onrender.com`. `https://…/health` doit répondre `{"status":"ok"}`.

Ensuite, chaque fusion sur `main` redéploie le site automatiquement. Ce qu'implique l'offre gratuite :

- le service s'endort après une quinzaine de minutes sans visite ; la visite suivante attend environ une minute qu'il se réveille ;
- le disque est éphémère : après chaque réveil ou redéploiement, les catalogues CelesTrak sont téléchargés à nouveau ;
- le processeur est modeste, environ soixante fois plus lent qu'un ordinateur portable récent : la première visite d'un quart d'heure attend quelques secondes que « Ce soir » soit calculé, les suivantes non.

### Le relais des catalogues

CelesTrak ne répond pas à Render. Le workflow GitHub Actions « Relais des catalogues » (`.github/workflows/catalogues.yml`) télécharge donc les groupes « visual » et « last-30-days » au format OMM (CSV) toutes les deux heures, comme CelesTrak le demande, vérifie que chacun contient l'en-tête OMM et au moins un satellite, et remplace `visual.csv` et `last-30-days.csv` dans la release `catalogues` du dépôt. Sur Render, `LA_HAUT_CATALOG_URL` pointe vers `https://github.com/Ghoutibk/la-haut/releases/download/catalogues/{group}.csv`.

- Le workflow se lance aussi à la main (onglet **Actions** → **Relais des catalogues** → **Run workflow**) et à chaque modification de son fichier sur `main`.
- GitHub suspend les workflows programmés d'un dépôt public après 60 jours sans activité sur le dépôt : il faut alors le réactiver dans l'onglet **Actions**.
- Si le relais s'arrête, le site continue avec la dernière copie publiée, qui vieillit : les heures de passage se décalent peu à peu au fil des jours.
- Ne supprime pas la release `catalogues` : le site la lit.

### Recevoir les avis

Les avis arrivent en tickets du dépôt privé `Ghoutibk/la-haut-avis`, étiquetés `problème`, `idée` ou `autre`. GitHub te prévient à chaque nouveau ticket. Le site a besoin d'un jeton qui ne peut écrire que les tickets de ce dépôt :

1. Sur GitHub, ouvre [la création d'un jeton à accès fin](https://github.com/settings/personal-access-tokens/new). Nomme-le `la-haut avis` et choisis une durée de validité.
2. **Repository access** → **Only select repositories** → `la-haut-avis`.
3. **Permissions** → **Repository permissions** → **Issues** : **Read and write**. Rien d'autre.
4. Génère le jeton et copie-le.
5. Sur Render, dans le service `la-haut` → **Environment**, donne sa valeur à `LA_HAUT_FEEDBACK_TOKEN`, puis enregistre : le service redémarre.

Sans jeton, la fenêtre d'avis répond que l'envoi est indisponible. Le message d'un visiteur est placé dans un bloc de code, où une mention `@quelqu'un` ne notifie personne. Un champ caché piège les robots, et au-delà de 20 avis par heure, le site demande d'attendre. À l'expiration du jeton, les avis cessent d'arriver : il faut en créer un nouveau.

## Architecture

Clean Architecture : les dépendances pointent vers le domaine, jamais l'inverse. La règle est vérifiée par `tests/unit/test_architecture.py`.

```
src/la_haut/
├── domain/          règles métier pures, aucune dépendance technique
├── application/     cas d'usage et ports (typing.Protocol)
├── infrastructure/  adaptateurs : Skyfield (satellites et planètes), fichier TLE, CSV OMM, téléchargement CelesTrak
├── interface/       API HTTP (FastAPI) et page web, branchées sur les cas d'usage seulement
└── composition.py   racine de composition : branche les adaptateurs sur les cas d'usage
```

## Langage omniprésent

| Métier | Code | Sens |
|---|---|---|
| Observateur | `Observer` | Qui regarde le ciel, à une latitude et une longitude |
| Fenêtre d'observation | `TimeWindow` | La période où l'on cherche des passages |
| Satellite | `Satellite` | Un objet en orbite, identifié par son numéro NORAD |
| Éléments orbitaux | `TwoLineElements` | L'orbite au format TLE, avec sommes de contrôle vérifiées |
| Éléments orbitaux moyens | `OrbitMeanElements` | L'orbite au format OMM du CCSDS, telle que CelesTrak la publie, champ par champ vérifié ; accepte les numéros NORAD au-delà de 99999 |
| Échantillon de ciel | `SkySample` | Où se trouve le satellite à un instant, éclairé ou non |
| Point cardinal | `CompassPoint` | Une des huit directions de la rose des vents |
| Visée | `compass.js` : `headingFrom`, `compassPointOf` | Le cap vers lequel pointe le haut du téléphone tenu à plat, rangé dans les mêmes huit secteurs que `CompassPoint` |
| Visibilité à l'œil nu | `NakedEyeVisibility` | Éclairé par le Soleil, à 10° ou plus, Soleil à −6° ou moins |
| Passage visible | `VisiblePass` | De l'apparition à la disparition, avec les directions |
| Satellite célèbre | `is_famous`, `FamousSatelliteCatalog` | ISS, Tiangong ou Hubble, reconnus à leur numéro NORAD : les seuls annoncés pour l'instant |
| Signalement | `Sighting` | « J'ai vu une lumière à telle heure, dans telle direction » |
| Directions voisines | `CompassPoint.is_close_to` | Le même point cardinal ou l'un de ses deux voisins : une direction donnée à l'œil |
| Écart au signalement | `VisiblePass.gap_to` | Temps entre le signalement et le moment où le passage était dans cette direction, à 5 minutes près |
| Objets amarrés | `docked_with`, `merge_docked_passes` | Passages qui coïncident à 30 s et 1° près : un seul point lumineux, un seul passage annoncé |
| Lancement | `TwoLineElements.launch`, `OrbitMeanElements.launch` | L'année et le numéro du lancement (désignation internationale sans la lettre de la pièce), communs à tous les objets d'un même tir |
| Starlink | `is_starlink`, `StarlinkCatalog` | Un satellite de la constellation Starlink, reconnu à son nom CelesTrak |
| Train Starlink | `gather_starlink_trains`, `VisiblePass.is_starlink_train`, `train_size` | Les Starlink d'un même lancement dont les passages se chevauchent sur le même chemin : une file de points, un seul passage annoncé. À la différence d'objets amarrés, ils se suivent à quelques secondes l'un de l'autre |
| Catalogue de satellites | `SatelliteCatalog` | Port : les satellites suivis |
| Catalogue combiné | `CombinedSatelliteCatalog` | Plusieurs catalogues réunis, chaque numéro NORAD une seule fois ; un catalogue indisponible n'empêche pas d'annoncer les autres |
| Traqueur de ciel | `SkyTracker` | Port : la trace d'un satellite dans le ciel de l'observateur, tant qu'il est au-dessus de l'horizon |
| Balayage | `SCAN_STEP` | Le premier passage du traqueur, toutes les minutes, qui trouve quand un satellite est au-dessus de l'horizon |
| Créneau | `ListVisiblePassesBySlot`, `SLOT` | Un quart d'heure : « Ce soir » se calcule une fois par créneau et par observateur |
| Planète | `Planet` | Vénus, Jupiter, Mars ou Saturne : les planètes brillantes que l'on prend pour un satellite ou un avion |
| Position d'une planète | `PlanetPosition` | Où se trouve une planète dans le ciel de l'observateur à un instant, avec la hauteur du Soleil |
| Écart à la direction | `PlanetPosition.angle_to`, `CompassPoint.azimuth_deg` | Angle entre la planète et le milieu de la direction signalée ; aucun si elle était sous l'horizon, dans un ciel trop clair ou ailleurs |
| Localisateur de planètes | `PlanetLocator` | Port : la position d'une planète vue par l'observateur à un instant |
| Candidat | `SightingIdentification` | Ce que propose « C'était quoi, ça ? » : un passage (satellite ou train Starlink) ou une planète, les satellites d'abord |
| Identification | `Identification` | La réponse à « C'était quoi, ça ? » : les candidats, du plus au moins probable |
| Satellites vérifiés | `Identification.satellites_checked` | Faux quand le catalogue des satellites manquait : seules les planètes ont été cherchées, et la page le dit |
| Avis | `Feedback` | Un message d'un visiteur à l'auteur du site, avec son e-mail facultatif pour une réponse |
| Nature de l'avis | `FeedbackKind` | Un problème, une idée ou autre chose |
| Boîte à avis | `FeedbackInbox` | Port : là où l'avis est remis ; en ligne, les tickets du dépôt privé |
| Plafond horaire | `MAX_FEEDBACK_PER_HOUR` | Au plus 20 avis remis par heure, contre les envois en masse |
| Délai avant nouvel essai | `CELESTRAK_RETRY_DELAY` | Après un téléchargement raté, le temps pendant lequel CelesTrak n'est pas redemandé |
| Relais des catalogues | `LA_HAUT_CATALOG_URL`, release `catalogues` | Une copie des groupes CelesTrak, servie un fichier `<groupe>.csv` par groupe, là où CelesTrak ne répond pas |

## Tests

| Famille | Cible | Où | Ce qu'on teste |
|---|---|---|---|
| Unitaires | 80 % | `tests/unit` | Domaine et cas d'usage, avec des doublures des ports |
| Intégration | 13 % | `tests/integration` | Adaptateurs branchés sur Skyfield et sur de vrais fichiers |
| Fonctionnels | 7 % | `tests/functional` | Scénarios Gherkin en français, de bout en bout |
| Page web | hors pyramide | `tests/js` | La logique de la page sans le navigateur, avec le lanceur de tests de Node : `node --test 'tests/js/**/*.test.js'` |

La répartition s'affiche à la fin de chaque `pytest`. Les valeurs de référence astronomiques viennent de calculs Skyfield indépendants de nos adaptateurs, sur un vrai TLE de l'ISS et sur les vrais catalogues CelesTrak du 6 octobre 2026 (`tests/support/celestrak`). Les builders et doublures partagés sont dans `tests/support`.

## Conventions

- **TDD et baby steps** : un test rouge, le code minimal pour le rendre vert, un refactoring si besoin, un commit.
- **SOLID** : une responsabilité par classe, des ports petits et ciblés, des cas d'usage qui dépendent d'abstractions, de nouveaux adaptateurs sans toucher aux cas d'usage.
- **KISS et DRY** : la solution la plus simple qui passe les tests, une seule source pour chaque connaissance.
- **Nommage** : PEP 8 vérifié par ruff (règles `N`). Modules en `snake_case`, classes en `PascalCase`, constantes en `UPPER_SNAKE_CASE`, exceptions suffixées par `Error`. Code en anglais, scénarios et documentation en français.
- **Conventional Commits** : `type(scope): description`, vérifié par le hook `commit-msg`. Les scopes suivent les couches : `domain`, `application`, `infrastructure`, `composition`, `architecture`.
- **Branches et PR** : une branche par fonctionnalité (`feat/...`), un titre de PR au format Conventional Commits, le modèle dans `.github/pull_request_template.md`.

## Limites connues

- Seuls les satellites célèbres et les Starlink récents sont annoncés. Le calcul de magnitude passage par passage, qui permettra d'en annoncer d'autres, reste à faire.
- Un Starlink isolé lancé dans les 30 derniers jours est annoncé sous son nom de catalogue, sans savoir s'il est réellement assez brillant.
- Suivre quelques centaines de Starlink sur 12 heures prend plusieurs secondes de calcul (environ 5 s pour 200 satellites sur un poste de développement) : l'onglet « Ce soir » peut être lent sur un petit serveur.
- « C'était quoi, ça ? » reconnaît les satellites suivis, les trains Starlink et quatre planètes. Un avion ou une étoile donnent « ni satellite ni planète ». Mercure, la Lune et les étoiles brillantes ne sont pas proposées.
- L'aspect de la lumière (un point, une file, un clignotement) n'est pas encore utilisé : une file de points vue au même endroit qu'une planète donne d'abord le satellite, puis la planète.
- Une planète est proposée dès que le Soleil est à −6° ou moins, même si Vénus se voit parfois plus tôt au crépuscule.
- Le JavaScript de la page n'a pas de tests automatisés : sa logique est volontairement réduite à l'affichage, le reste est testé côté Python.
