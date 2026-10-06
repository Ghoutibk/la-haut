# Là-haut

Ce qui passe au-dessus de toi ce soir : les satellites visibles à l'œil nu depuis chez toi, et la réponse à « c'était quoi, cette lumière ? ».

## Ce que fait Là-haut aujourd'hui

Pour un observateur et une période, Là-haut liste les passages visibles à l'œil nu des satellites célèbres (l'ISS, Tiangong et Hubble) et des trains Starlink. Les éléments orbitaux viennent de deux groupes CelesTrak, téléchargés au besoin et gardés deux heures en cache chacun : « visual » pour les satellites célèbres, « last-30-days » pour les Starlink lancés dans les 30 derniers jours. Attention : depuis mi-2026, les objets nouvellement lancés reçoivent des numéros NORAD au-delà de 99999, que le format TLE ne sait pas écrire. CelesTrak ne publie donc plus « last-30-days » qu'en CSV, JSON ou XML (OMM), et répond 404 en TLE : les trains Starlink ne sont pas annoncés avec les vraies données tant que Là-haut ne lit pas ces formats. Si un groupe est injoignable et sans cache, l'autre continue d'être annoncé. Après un téléchargement raté, CelesTrak n'est pas redemandé avant 15 minutes : les visites suivantes répondent tout de suite, avec le dernier catalogue connu s'il existe. Chaque échec est écrit dans les logs avec sa cause. Le calcul des passages tourne hors ligne : propagation SGP4 et position du Soleil avec Skyfield, éphémérides DE421 embarquées. Les objets amarrés ensemble sont annoncés comme un seul passage. Les Starlink d'un même lancement qui défilent en file sur le même chemin le sont aussi, sous le nom « Train Starlink (N satellites) » : c'est la file de points que l'on prend pour des OVNI.

À partir d'un signalement (« j'ai vu une lumière à telle heure, direction sud-est »), Là-haut retrouve aussi ce qui était là : c'est « C'était quoi, ça ? ». Il cherche d'abord parmi les satellites suivis, trains Starlink compris, puis parmi les planètes brillantes que l'on prend souvent pour un satellite ou un avion : Vénus, Jupiter, Mars et Saturne. Une planète est candidate si elle était au-dessus de l'horizon, dans un ciel assez sombre (Soleil à −6° ou moins), dans la direction indiquée ou une direction voisine ; les planètes sont classées de la plus proche à la plus éloignée de cette direction, après les satellites. Leurs positions sont calculées hors ligne avec les éphémérides DE421 embarquées : sans aucun catalogue de satellites, les planètes répondent quand même, et la réponse précise que les satellites n'ont pas pu être vérifiés.

Les deux sont accessibles sur un site web : une page mobile avec les onglets « Ce soir » et « C'était quoi ? », appuyée sur une API HTTP.

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

Puis ouvre http://127.0.0.1:8000. La page demande ta position et se replie sur Paris si tu refuses ou ne réponds pas. Le cache CelesTrak se trouve dans `~/.cache/la-haut/visual.tle`, à côté de `last-30-days.tle` ; la variable d'environnement `LA_HAUT_CACHE` permet de déplacer les deux. `LA_HAUT_CATALOG_URL` change la source des catalogues : une adresse où `{group}` est remplacé par le nom du groupe, CelesTrak par défaut.

| Route | Rôle |
|---|---|
| `GET /` | La page web |
| `GET /health` | Vérification de santé pour l'hébergeur : répond 200 sans rien calculer |
| `GET /api/passes?latitude=&longitude=&hours=12` | Les passages visibles des prochaines heures (1 à 48) |
| `GET /api/identification?latitude=&longitude=&at=&direction=` | « C'était quoi, ça ? » : `at` en ISO 8601 avec fuseau, `direction` parmi N, NE, E, SE, S, SW, W, NW. Chaque candidat porte un `kind` : `satellite`, `train` ou `planet`. `satellites_checked` vaut `false` quand le catalogue des satellites manquait et que seules les planètes ont été cherchées |

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
- le processeur est modeste : l'onglet « Ce soir » peut mettre plusieurs secondes quand beaucoup de Starlink ont été lancés récemment.

### Le relais des catalogues

CelesTrak ne répond pas à Render. Le workflow GitHub Actions « Relais des catalogues » (`.github/workflows/catalogues.yml`) télécharge donc le groupe « visual » toutes les deux heures, comme CelesTrak le demande, vérifie qu'il contient des éléments orbitaux, et remplace `visual.tle` dans la release `catalogues` du dépôt. Sur Render, `LA_HAUT_CATALOG_URL` pointe vers `https://github.com/Ghoutibk/la-haut/releases/download/catalogues/{group}.tle`.

- Le workflow se lance aussi à la main (onglet **Actions** → **Relais des catalogues** → **Run workflow**) et à chaque modification de son fichier sur `main`.
- GitHub suspend les workflows programmés d'un dépôt public après 60 jours sans activité sur le dépôt : il faut alors le réactiver dans l'onglet **Actions**.
- Si le relais s'arrête, le site continue avec la dernière copie publiée, qui vieillit : les heures de passage se décalent peu à peu au fil des jours.
- Ne supprime pas la release `catalogues` : le site la lit.

## Architecture

Clean Architecture : les dépendances pointent vers le domaine, jamais l'inverse. La règle est vérifiée par `tests/unit/test_architecture.py`.

```
src/la_haut/
├── domain/          règles métier pures, aucune dépendance technique
├── application/     cas d'usage et ports (typing.Protocol)
├── infrastructure/  adaptateurs : Skyfield (satellites et planètes), fichier TLE, téléchargement CelesTrak
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
| Échantillon de ciel | `SkySample` | Où se trouve le satellite à un instant, éclairé ou non |
| Point cardinal | `CompassPoint` | Une des huit directions de la rose des vents |
| Visibilité à l'œil nu | `NakedEyeVisibility` | Éclairé par le Soleil, à 10° ou plus, Soleil à −6° ou moins |
| Passage visible | `VisiblePass` | De l'apparition à la disparition, avec les directions |
| Satellite célèbre | `is_famous`, `FamousSatelliteCatalog` | ISS, Tiangong ou Hubble, reconnus à leur numéro NORAD : les seuls annoncés pour l'instant |
| Signalement | `Sighting` | « J'ai vu une lumière à telle heure, dans telle direction » |
| Directions voisines | `CompassPoint.is_close_to` | Le même point cardinal ou l'un de ses deux voisins : une direction donnée à l'œil |
| Écart au signalement | `VisiblePass.gap_to` | Temps entre le signalement et le moment où le passage était dans cette direction, à 5 minutes près |
| Objets amarrés | `docked_with`, `merge_docked_passes` | Passages qui coïncident à 30 s et 1° près : un seul point lumineux, un seul passage annoncé |
| Lancement | `TwoLineElements.launch` | L'année et le numéro du lancement (désignation internationale sans la lettre de la pièce), communs à tous les objets d'un même tir |
| Starlink | `is_starlink`, `StarlinkCatalog` | Un satellite de la constellation Starlink, reconnu à son nom CelesTrak |
| Train Starlink | `gather_starlink_trains`, `VisiblePass.is_starlink_train`, `train_size` | Les Starlink d'un même lancement dont les passages se chevauchent sur le même chemin : une file de points, un seul passage annoncé. À la différence d'objets amarrés, ils se suivent à quelques secondes l'un de l'autre |
| Catalogue de satellites | `SatelliteCatalog` | Port : les satellites suivis |
| Catalogue combiné | `CombinedSatelliteCatalog` | Plusieurs catalogues réunis, chaque numéro NORAD une seule fois ; un catalogue indisponible n'empêche pas d'annoncer les autres |
| Traqueur de ciel | `SkyTracker` | Port : la trace d'un satellite dans le ciel de l'observateur |
| Planète | `Planet` | Vénus, Jupiter, Mars ou Saturne : les planètes brillantes que l'on prend pour un satellite ou un avion |
| Position d'une planète | `PlanetPosition` | Où se trouve une planète dans le ciel de l'observateur à un instant, avec la hauteur du Soleil |
| Écart à la direction | `PlanetPosition.angle_to`, `CompassPoint.azimuth_deg` | Angle entre la planète et le milieu de la direction signalée ; aucun si elle était sous l'horizon, dans un ciel trop clair ou ailleurs |
| Localisateur de planètes | `PlanetLocator` | Port : la position d'une planète vue par l'observateur à un instant |
| Candidat | `SightingIdentification` | Ce que propose « C'était quoi, ça ? » : un passage (satellite ou train Starlink) ou une planète, les satellites d'abord |
| Identification | `Identification` | La réponse à « C'était quoi, ça ? » : les candidats, du plus au moins probable |
| Satellites vérifiés | `Identification.satellites_checked` | Faux quand le catalogue des satellites manquait : seules les planètes ont été cherchées, et la page le dit |
| Délai avant nouvel essai | `CELESTRAK_RETRY_DELAY` | Après un téléchargement raté, le temps pendant lequel CelesTrak n'est pas redemandé |
| Relais des catalogues | `LA_HAUT_CATALOG_URL`, release `catalogues` | Une copie des groupes CelesTrak, servie un fichier `<groupe>.tle` par groupe, là où CelesTrak ne répond pas |

## Tests

| Famille | Cible | Où | Ce qu'on teste |
|---|---|---|---|
| Unitaires | 80 % | `tests/unit` | Domaine et cas d'usage, avec des doublures des ports |
| Intégration | 13 % | `tests/integration` | Adaptateurs branchés sur Skyfield et sur de vrais fichiers |
| Fonctionnels | 7 % | `tests/functional` | Scénarios Gherkin en français, de bout en bout |

La répartition s'affiche à la fin de chaque `pytest`. Les valeurs de référence astronomiques viennent de calculs Skyfield indépendants de nos adaptateurs, sur un vrai TLE de l'ISS. Les builders et doublures partagés sont dans `tests/support`.

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
