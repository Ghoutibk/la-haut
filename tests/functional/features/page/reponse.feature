# language: fr
Fonctionnalité: Lire sur la page ce qu'était la lumière
  En tant que curieux qui a vu une lumière traverser le ciel
  Je veux lire une réponse claire, avec l'heure et le chemin de ce qui passait
  Afin de comprendre ce que j'ai vu

  Contexte:
    Étant donné que nous sommes le 5 octobre 2026 à 21:30

  Scénario: C'était un satellite
    Étant donné que Là-haut y reconnaît ces passages :
      | satellite    | début | fin   | depuis | vers | hauteur |
      | CSS (TIANHE) | 21:12 | 21:16 | sud    | est  | 47      |
    Quand je signale une lumière vue à l'instant, direction « Sud-est »
    Alors la réponse est « Station spatiale chinoise Tiangong », sous « C'était très probablement »
    Et la réponse dit « Visible de 21:12 à 21:16, du sud vers l'est. »
    Et la réponse dit « Au plus haut à 47° au-dessus de l'horizon. »
    Et la réponse propose « Ce n'était pas ça ? Dis-le-nous »

  Scénario: C'était un train Starlink
    Étant donné que Là-haut y reconnaît ces passages :
      | satellite                      | début | fin   | depuis | vers     | hauteur |
      | train Starlink de 3 satellites | 21:05 | 21:12 | ouest  | nord-est | 34      |
    Quand je signale une lumière vue à l'instant, direction « Nord-ouest »
    Alors la réponse est « Train Starlink (3 satellites) », sous « C'était très probablement »
    Et la réponse dit « Visible de 21:05 à 21:12, de l'ouest vers le nord-est. »
    Et la réponse dit « Au plus haut à 34° au-dessus de l'horizon. »
    Et la réponse dit « Une file de points brillants qui se suivent : les satellites Starlink d'un même lancement, quelques jours après leur mise en orbite. »

  Scénario: C'était une planète, ou peut-être une autre
    Étant donné que Là-haut y reconnaît ces planètes :
      | planète | direction | hauteur |
      | Vénus   | ouest     | 12      |
      | Jupiter | sud-ouest | 25      |
    Quand je signale une lumière vue à l'instant, direction « Ouest »
    Alors la réponse est « Vénus », sous « C'était très probablement »
    Et la réponse dit « Vénus brillait vers l'ouest, à 12° au-dessus de l'horizon. »
    Et la réponse dit « Une planète ne bouge pas en quelques minutes : elle reste au même endroit parmi les étoiles. Si ta lumière filait dans le ciel, c'était plutôt un satellite ou un avion. »
    Et la réponse dit « Ou peut-être : Jupiter. »
    Et la réponse propose « Ce n'était pas ça ? Dis-le-nous »

  Scénario: Un satellite passe avant les planètes vues dans la même direction
    Étant donné que Là-haut y reconnaît ces passages :
      | satellite    | début | fin   | depuis | vers | hauteur |
      | CSS (TIANHE) | 21:12 | 21:16 | sud    | est  | 47      |
    Et que Là-haut y reconnaît ces planètes :
      | planète | direction | hauteur |
      | Mars    | sud-est   | 18      |
      | Saturne | sud       | 30      |
    Quand je signale une lumière vue à l'instant, direction « Sud-est »
    Alors la réponse est « Station spatiale chinoise Tiangong », sous « C'était très probablement »
    Et la réponse dit « Ou peut-être : Mars, Saturne. »

  Scénario: Sans catalogue de satellites, une planète n'est que peut-être la réponse
    Étant donné que Là-haut y reconnaît ces planètes :
      | planète | direction | hauteur |
      | Saturne | sud       | 20      |
    Et que Là-haut n'a pas pu vérifier les satellites
    Quand je signale une lumière vue à l'instant, direction « Sud »
    Alors la réponse est « Saturne », sous « C'était peut-être »
    Et la réponse dit « Saturne brillait vers le sud, à 20° au-dessus de l'horizon. »
    Et la réponse dit « Le catalogue des satellites est indisponible pour le moment : seules les planètes ont été vérifiées. Réessaie plus tard pour savoir si c'était un satellite. »
    Et la réponse propose « Ce n'était pas ça ? Dis-le-nous »

  Scénario: Ni satellite ni planète
    Quand je signale une lumière vue à l'instant, direction « Nord »
    Alors la réponse est « Ni satellite ni planète », sous « Rien de connu »
    Et la réponse dit « Aucun satellite suivi ni aucune planète brillante n'était dans cette direction à ce moment. C'était peut-être un avion ou une étoile. »
    Et la réponse propose « Ce n'était pas ça ? Dis-le-nous »

  Scénario: Pas une planète, et les satellites n'ont pas pu être vérifiés
    Étant donné que Là-haut n'a pas pu vérifier les satellites
    Quand je signale une lumière vue à l'instant, direction « Nord »
    Alors la réponse est « Pas une planète », sous « Rien de connu »
    Et la réponse dit « Aucune planète brillante n'était dans cette direction à ce moment. »
    Et la réponse dit « Le catalogue des satellites est indisponible pour le moment : seules les planètes ont été vérifiées. Réessaie plus tard pour savoir si c'était un satellite. »
    Et la réponse propose « Ce n'était pas ça ? Dis-le-nous »
