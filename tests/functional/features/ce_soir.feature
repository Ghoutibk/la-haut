# language: fr
Fonctionnalité: Savoir ce que « Ce soir » annonce, et sous quel nom
  En tant que curieux qui lève les yeux le soir
  Je veux que « Ce soir » n'annonce que ce que je saurai reconnaître, sous un nom que je comprends
  Afin de savoir quoi chercher dans le ciel

  Contexte:
    Étant donné un observateur à Paris
    Et CelesTrak publie ses catalogues du 6 octobre 2026 au format OMM

  Scénario: La station chinoise est annoncée sous son nom public
    Quand j'ouvre « Ce soir » le 7 octobre 2026 à 6 h
    Alors « Ce soir » annonce « Station spatiale chinoise Tiangong » le 7 octobre 2026 de 06:41 à 06:45

  Scénario: Un Starlink récent qui passe seul est annoncé sous son nom de catalogue
    Quand j'ouvre « Ce soir » le 7 octobre 2026 à 6 h
    Alors « Ce soir » annonce « STARLINK-38375 » le 7 octobre 2026 de 06:16 à 06:19

  Scénario: Seuls les satellites célèbres et les Starlink récents sont annoncés
    # Le groupe « visual » compte des dizaines d'autres objets visibles ce matin-là, comme le corps
    # de fusée H-2A R/B, qui passe de 06:41 à 06:47, en même temps que la station chinoise.
    Quand j'ouvre « Ce soir » le 7 octobre 2026 à 6 h
    Alors « Ce soir » n'annonce que la station chinoise et des Starlink
