# language: fr
Fonctionnalité: Lire sur la page les passages de ce soir
  En tant que curieux qui lève les yeux le soir
  Je veux lire l'heure, le nom et le chemin de chaque passage
  Afin de savoir quand et où regarder

  Contexte:
    Étant donné que nous sommes le 5 octobre 2026 à 21:30

  Scénario: Les passages sont annoncés du plus proche au plus lointain
    Étant donné que Là-haut annonce ces passages :
      | satellite                      | jour           | début | fin   | depuis | vers     | hauteur |
      | CSS (TIANHE)                   | 5 octobre 2026 | 21:42 | 21:46 | sud    | est      | 17      |
      | train Starlink de 3 satellites | 6 octobre 2026 | 05:49 | 05:56 | ouest  | nord-est | 34      |
    Quand j'ouvre Là-haut
    Alors la vue « Au-dessus de toi » annonce « Les satellites célèbres et les trains Starlink visibles à l'œil nu dans les 12 prochaines heures. »
    Et je vois ces passages :
      | heure | jour            | nom                                | chemin                   | hauteur                                   |
      | 21:42 |                 | Station spatiale chinoise Tiangong | sud → est · 4 min        | Au plus haut à 17° au-dessus de l'horizon |
      | 05:49 | mardi 6 octobre | Train Starlink (3 satellites)      | ouest → nord-est · 7 min | Au plus haut à 34° au-dessus de l'horizon |
    Et le passage « Train Starlink (3 satellites) » explique « Une file de points brillants qui se suivent : les satellites Starlink d'un même lancement, quelques jours après leur mise en orbite. »

  Plan du scénario: La durée d'un passage est arrondie à la minute, une minute au moins
    Étant donné que Là-haut annonce ces passages :
      | satellite    | jour           | début    | fin   | depuis | vers    | hauteur |
      | CSS (TIANHE) | 5 octobre 2026 | 21:42:00 | <fin> | sud    | sud-est | 11      |
    Quand j'ouvre Là-haut
    Alors je vois ces passages :
      | heure | jour | nom                                | chemin    | hauteur                                   |
      | 21:42 |      | Station spatiale chinoise Tiangong | <chemin>  | Au plus haut à 11° au-dessus de l'horizon |

    Exemples:
      | fin      | chemin                  |
      | 21:42:20 | sud → sud-est · 1 min   |
      | 21:46:40 | sud → sud-est · 5 min   |

  Scénario: Aucun passage visible cette nuit
    Quand j'ouvre Là-haut
    Alors la vue « Au-dessus de toi » annonce « Aucun passage visible dans les 12 prochaines heures. Les satellites se voient surtout peu après le coucher du soleil et avant l'aube. »
    Et je ne vois aucun passage

  Scénario: La page patiente pendant que Là-haut cherche les passages
    Étant donné que Là-haut met du temps à chercher les passages
    Quand j'ouvre Là-haut
    Alors la vue « Au-dessus de toi » annonce « Recherche des passages… »
    Quand Là-haut répond enfin
    Alors la vue « Au-dessus de toi » annonce « Aucun passage visible dans les 12 prochaines heures. Les satellites se voient surtout peu après le coucher du soleil et avant l'aube. »

  Plan du scénario: La page dit pourquoi elle ne peut pas annoncer les passages
    Étant donné que <panne>
    Quand j'ouvre Là-haut
    Alors la vue « Au-dessus de toi » annonce « <explication> »
    Et je ne vois aucun passage

    Exemples:
      | panne                                         | explication                                                                     |
      | le catalogue des satellites est indisponible  | Le catalogue des satellites est indisponible pour le moment, réessaie plus tard. |
      | l'hébergeur de Là-haut est en panne           | Le ciel est injoignable pour le moment.                                         |
