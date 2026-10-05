# language: fr
Fonctionnalité: Voir les passages visibles au-dessus de chez moi
  En tant que curieux qui lève les yeux le soir
  Je veux savoir quand un satellite passera visiblement au-dessus de moi
  Afin de ne pas rater son passage

  Contexte:
    Étant donné un observateur à Paris
    Et un catalogue qui suit l'ISS avec ses éléments orbitaux du 3 juillet 2018

  Scénario: L'ISS se montre juste avant l'aube
    Quand je cherche les passages visibles du 4 juillet 2018 à 3 h au 4 juillet 2018 à 6 h
    Alors je vois ces passages :
      | satellite   | jour           | début | fin   | depuis | vers |
      | ISS (ZARYA) | 4 juillet 2018 | 04:54 | 04:58 | sud    | est  |

  Scénario: Les passages de plusieurs nuits sont annoncés du plus proche au plus lointain
    Quand je cherche les passages visibles du 4 juillet 2018 à 0 h au 7 juillet 2018 à 0 h
    Alors je vois ces passages :
      | satellite   | jour           | début | fin   | depuis | vers |
      | ISS (ZARYA) | 4 juillet 2018 | 04:54 | 04:58 | sud    | est  |
      | ISS (ZARYA) | 6 juillet 2018 | 04:45 | 04:51 | sud    | est  |

  Scénario: Un vaisseau amarré à l'ISS ne crée pas de doublon
    Étant donné un vaisseau amarré à l'ISS dans le catalogue
    Quand je cherche les passages visibles du 4 juillet 2018 à 3 h au 4 juillet 2018 à 6 h
    Alors je vois ces passages :
      | satellite   | jour           | début | fin   | depuis | vers |
      | ISS (ZARYA) | 4 juillet 2018 | 04:54 | 04:58 | sud    | est  |
    Et le vaisseau amarré est signalé avec l'ISS

  Plan du scénario: Rien n'est annoncé quand le ciel est trop clair pour voir l'ISS
    Quand je cherche les passages visibles du <début> au <fin>
    Alors je ne vois aucun passage

    Exemples:
      | début                | fin                   | ciel             |
      | 5 juillet 2018 à 5 h | 5 juillet 2018 à 6 h  | aube déjà claire |
      | 4 juillet 2018 à 6 h | 4 juillet 2018 à 12 h | plein jour       |
