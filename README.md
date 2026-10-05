# Là-haut

Ce qui passe au-dessus de toi ce soir : les satellites visibles à l'œil nu depuis chez toi, et la réponse à « c'était quoi, cette lumière ? ».

## Démarrer

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

## Conventions

- **TDD** : pas une ligne de code de production sans un test rouge d'abord.
- **Baby steps** : un petit pas, un test vert, un commit.
- **Conventional Commits** : `type(scope): description`, vérifié par le hook `commit-msg`.
- **Pyramide de tests** : environ 80 % unitaires, 13 % d'intégration, 7 % fonctionnels. Le rapport s'affiche à la fin de chaque `pytest`.
