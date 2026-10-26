# language: fr
Fonctionnalité: Garder la page immobile quand les animations me gênent
  En tant que visiteur que les mouvements à l'écran gênent
  Je veux que les boutons ne bougent pas quand mon téléphone demande de réduire les animations
  Afin d'utiliser Là-haut sans inconfort

  Plan du scénario: Un bouton se tasse sous le doigt, sauf si je préfère réduire les animations
    Étant donné que <préférence>
    Quand j'ouvre l'adresse #cetait-quoi
    Et j'appuie sans relâcher sur « <bouton> »
    Alors le bouton « <bouton> » <effet>

    Exemples:
      | préférence                                    | bouton     | effet           |
      | je n'ai pas de préférence pour les animations | Nord       | rapetisse       |
      | je n'ai pas de préférence pour les animations | Identifier | rapetisse       |
      | je préfère réduire les animations             | Nord       | garde sa taille |
      | je préfère réduire les animations             | Identifier | garde sa taille |
