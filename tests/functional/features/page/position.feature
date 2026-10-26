# language: fr
Fonctionnalité: Chercher les passages depuis là où je suis
  En tant que curieux qui lève les yeux le soir
  Je veux que Là-haut cherche les passages au-dessus de chez moi, sans rien taper
  Afin de voir ce qui passera vraiment au-dessus de ma tête

  Scénario: J'accepte de donner ma position
    Étant donné que je suis à Lyon, en 45.764043, 4.835659, et que j'accepte de donner ma position
    Quand j'ouvre Là-haut
    Alors l'en-tête indique « Ta position »
    Et Là-haut cherche les passages des 12 prochaines heures en 45.76, 4.84

  Plan du scénario: Sans ma position, Là-haut cherche au-dessus de Paris
    Étant donné que <situation>
    Quand j'ouvre Là-haut
    Alors l'en-tête indique « Paris »
    Et Là-haut cherche les passages des 12 prochaines heures au-dessus de Paris

    Exemples:
      | situation                               |
      | je refuse de donner ma position         |
      | mon navigateur ne sait pas me localiser |

  Scénario: Je ne réponds pas à la demande de position
    Étant donné que je ne réponds pas à la demande de position
    Quand j'ouvre Là-haut
    Alors l'en-tête indique « Paris »
    Et la vue « Au-dessus de toi » annonce « Recherche des passages… »
    Et Là-haut n'a encore cherché aucun passage
    Quand 6 secondes passent
    Alors Là-haut cherche les passages des 12 prochaines heures au-dessus de Paris
