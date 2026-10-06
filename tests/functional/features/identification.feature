# language: fr
Fonctionnalité: Savoir ce qu'était la lumière que j'ai vue
  En tant que curieux qui a vu une lumière traverser le ciel
  Je veux dire quand et où je l'ai vue
  Afin de savoir quel satellite c'était

  Contexte:
    Étant donné un observateur à Paris
    Et un catalogue qui suit l'ISS avec ses éléments orbitaux du 3 juillet 2018

  Plan du scénario: Je retrouve l'ISS que j'ai vue passer avant l'aube
    Quand j'ai vu une lumière le 4 juillet 2018 à <heure>, direction <direction>
    Alors c'était ISS (ZARYA)

    Exemples:
      | heure | direction | moment                          |
      | 04:55 | sud       | elle venait d'apparaître        |
      | 04:56 | sud-est   | au plus haut de son passage     |
      | 04:59 | est       | je raconte un peu après coup    |

  Plan du scénario: Une lumière vue ailleurs ou à un autre moment n'était pas un satellite connu
    Quand j'ai vu une lumière le 4 juillet 2018 à <heure>, direction <direction>
    Alors ce n'était aucun satellite connu

    Exemples:
      | heure | direction  | raison                            |
      | 04:56 | nord-ouest | à l'opposé de l'ISS               |
      | 05:15 | est        | l'ISS avait disparu depuis 17 min |

  Plan du scénario: Je reconnais une planète, immobile dans un ciel assez sombre
    Quand j'ai vu une lumière le <jour> à <heure>, direction <direction>
    Alors la lumière était la planète <planète>

    Exemples:
      | jour           | heure | direction | planète | ciel                                         |
      | 3 juillet 2018 | 22:45 | ouest     | Vénus   | l'étoile du berger, basse après le coucher   |
      | 4 juillet 2018 | 01:00 | sud       | Saturne | Mars au sud-est et Jupiter au sud-ouest aussi |
      | 4 juillet 2018 | 01:00 | sud-ouest | Jupiter | Saturne au sud, voisin                       |
      | 4 juillet 2018 | 03:00 | sud       | Mars    | Saturne au sud-ouest, voisin                 |

  Scénario: Un satellite passe avant une planète vue dans la même direction
    Quand j'ai vu une lumière le 4 juillet 2018 à 04:56, direction sud-est
    Alors c'était ISS (ZARYA)
    Et sinon, c'était la planète Mars
