# Là-haut

Ce qui passe au-dessus de toi ce soir : les satellites visibles à l'œil nu depuis chez toi, et la réponse à « c'était quoi, cette lumière ? ».

## Ce que fait cette première tranche

Pour un observateur et une période, Là-haut liste les passages visibles à l'œil nu des satellites d'un catalogue au format CelesTrak. Le calcul tourne hors ligne : propagation SGP4 et position du Soleil avec Skyfield, éphémérides DE421 embarquées.

## Démarrer

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

## Architecture

Clean Architecture : les dépendances pointent vers le domaine, jamais l'inverse. La règle est vérifiée par `tests/unit/test_architecture.py`.

```
src/la_haut/
├── domain/          règles métier pures, aucune dépendance technique
├── application/     cas d'usage et ports (typing.Protocol)
├── infrastructure/  adaptateurs : Skyfield, fichier TLE CelesTrak
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
| Catalogue de satellites | `SatelliteCatalog` | Port : les satellites suivis |
| Traqueur de ciel | `SkyTracker` | Port : la trace d'un satellite dans le ciel de l'observateur |

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

- La luminosité n'est pas encore prise en compte : un petit satellite éclairé compte comme visible.
- Le catalogue se lit depuis un fichier ; le téléchargement depuis CelesTrak reste à brancher.
- L'identification « c'était quoi ? », l'API et l'interface viendront dans les prochaines tranches.
