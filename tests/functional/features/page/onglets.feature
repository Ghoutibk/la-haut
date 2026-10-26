# language: fr
Fonctionnalité: Passer de « Ce soir » à « C'était quoi ? »
  En tant que curieux qui lève les yeux le soir
  Je veux passer d'un onglet à l'autre en bas de l'écran
  Afin de voir les passages de ce soir ou de dire ce que j'ai vu

  Scénario: « Ce soir » s'ouvre par défaut
    Quand j'ouvre Là-haut
    Alors je vois la vue « Au-dessus de toi »
    Et la vue « Tu as vu une lumière bouger dans le ciel ? » est cachée
    Et l'onglet « Ce soir » est l'onglet actif
    Et l'onglet « C'était quoi ? » ne l'est pas

  Plan du scénario: Chaque adresse ouvre son onglet, une adresse inconnue ouvre « Ce soir »
    Quand j'ouvre l'adresse <adresse>
    Alors je vois la vue « <vue> »
    Et l'onglet « <onglet> » est l'onglet actif

    Exemples:
      | adresse         | vue                                        | onglet         |
      | #ce-soir        | Au-dessus de toi                           | Ce soir        |
      | #cetait-quoi    | Tu as vu une lumière bouger dans le ciel ? | C'était quoi ? |
      | #n-importe-quoi | Au-dessus de toi                           | Ce soir        |

  Scénario: Je passe à l'autre onglet, puis je reviens à la page précédente
    Quand j'ouvre Là-haut
    Et je touche l'onglet « C'était quoi ? »
    Alors je vois la vue « Tu as vu une lumière bouger dans le ciel ? »
    Et la vue « Au-dessus de toi » est cachée
    Et l'onglet « C'était quoi ? » est l'onglet actif
    Et l'onglet « Ce soir » ne l'est pas
    Et l'adresse de la page finit par #cetait-quoi
    Quand je reviens à la page précédente
    Alors je vois la vue « Au-dessus de toi »
    Et l'onglet « Ce soir » est l'onglet actif
