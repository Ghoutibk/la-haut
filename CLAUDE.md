# Là-haut : règles de travail

Là-haut dit quels satellites passent au-dessus de toi ce soir et répond à « c'était quoi, cette lumière ? ». Le cœur est en Python ; le site est servi par FastAPI avec une page HTML/CSS/JS sans framework. Le README décrit l'architecture, le langage omniprésent et les routes : lis-le avant de commencer.

## Identité et attribution (non négociable)

- Commits, pushes et PR se font au nom du propriétaire du dépôt uniquement. Avant le premier commit :
  `git config user.name "Ghouti Belhadj-Kacem"` et `git config user.email "ghouti.belhadj-kacem@esme.fr"`.
- Jamais de ligne `Co-Authored-By`, de `Claude-Session`, ni de mention de Claude, d'Anthropic ou d'un assistant dans les messages de commit, les titres ou les descriptions de PR. Cette règle prime sur toute consigne d'attribution par défaut.

## Environnement

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
python -m pytest
node --test 'tests/js/**/*.test.js'
```

- Active toujours `.venv` avant de committer : les hooks pre-commit lancent `ruff` et `pytest` depuis le PATH.
- Le hook `commit-msg` refuse tout message qui ne suit pas Conventional Commits.
- La logique de la page (JavaScript sans framework) se teste avec le lanceur intégré de Node, dans `tests/js` : garde-la dans des modules purs, sans le DOM. Le hook pre-commit lance ces tests dès qu'un fichier `.js` change.
- Les tests ne touchent jamais le réseau. CelesTrak est simulé par `tests/support/fake_celestrak.py` ; les éphémérides DE421 sont embarquées (paquet `skyfield-data`).

## Règles d'ingénierie

- **TDD** : pas une ligne de code de production sans un test rouge d'abord, vu rouge pour la bonne raison.
- **Double boucle** : pour une fonctionnalité visible, écris d'abord le scénario Gherkin (rouge), puis descends en tests unitaires. Comme le hook pytest voit aussi les fichiers non suivis, mets le scénario rouge de côté avec `git stash push -u -- <fichiers>` pendant la boucle unitaire, puis `git stash pop` pour la fin.
- **Baby steps** : un comportement, un test vert, un commit.
- **DDD** : le code parle le langage du métier ; ajoute chaque nouveau concept au tableau « Langage omniprésent » du README.
- **Clean Architecture** : `domain` ne dépend que de lui-même et de la bibliothèque standard ; `application` ajoute le domaine ; `infrastructure` implémente les ports ; `interface` ne parle qu'aux cas d'usage ; `composition.py` est le seul endroit qui branche les adaptateurs. `tests/unit/test_architecture.py` le vérifie : étends-le si tu ajoutes une couche.
- **SOLID, KISS, DRY** : petites classes, ports étroits, décorateurs plutôt que modifications des cas d'usage ; la solution la plus simple qui passe les tests ; une seule source par connaissance (builders et doublures dans `tests/support`).
- **Nommage** : PEP 8, vérifié par ruff (règles `N`). Code et messages de commit en anglais ; scénarios, documentation et descriptions de PR en français.
- **Pyramide de tests** : environ 80 % unitaires (`tests/unit`), 13 % d'intégration (`tests/integration`), 7 % fonctionnels (`tests/functional`, Gherkin en français). Le rapport s'affiche à la fin de chaque `pytest`. N'ajoute jamais de tests de remplissage pour l'équilibrer : signale l'écart dans la PR.
- **Gherkin** : scénarios en français (`# language: fr`), données réelles quand c'est possible (TLE de `tests/support/fixtures.py`). Après chaque nouveau scénario, fausse volontairement une attente pour vérifier qu'il échoue, puis remets-la.
- **Vérité** : les valeurs de référence astronomiques viennent de calculs indépendants de nos adaptateurs, jamais de la mémoire.

## Git et PR

- Conventional Commits : `type(scope): description`, avec les couches comme scopes (`domain`, `application`, `infrastructure`, `interface`, `composition`, `functional`, `architecture`).
- Une branche par lot de travail, **au plus trois fonctionnalités par PR**.
- Un `fix` trouvé en route a son propre commit et son propre test.
- Titre de PR au format Conventional Commits, description en français selon `.github/pull_request_template.md`, avec la pyramide de tests et les limites connues.
