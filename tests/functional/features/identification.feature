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
