# language: fr
Fonctionnalité: Dire sur la page quand et où j'ai vu une lumière
  En tant que curieux qui a vu une lumière traverser le ciel
  Je veux dire en quelques gestes quand et dans quelle direction je l'ai vue
  Afin que Là-haut cherche ce qui était là

  Contexte:
    Étant donné que nous sommes le 5 octobre 2026 à 21:30

  Scénario: Je signale une lumière vue à l'instant
    Quand j'ouvre l'adresse #cetait-quoi
    Alors seul « À l'instant » est choisi parmi « Quand ? »
    Et je ne vois pas le champ « Heure à laquelle tu l'as vue »
    Quand je choisis la direction « Nord-est »
    Et je demande à identifier ma lumière
    Alors Là-haut cherche ce qui était au nord-est le 5 octobre 2026 à 21:30:00, au-dessus de Paris

  Scénario: « Il y a 15 min » se compte au moment où j'envoie
    Quand j'ouvre l'adresse #cetait-quoi
    Et je dis l'avoir vue « Il y a 15 min »
    Et je choisis la direction « Sud »
    Et 5 minutes passent
    Et je demande à identifier ma lumière
    Alors seul « Il y a 15 min » est choisi parmi « Quand ? »
    Et Là-haut cherche ce qui était au sud le 5 octobre 2026 à 21:20:00, au-dessus de Paris

  Scénario: Je l'ai vue plus tôt dans la soirée
    Quand j'ouvre l'adresse #cetait-quoi
    Et je dis l'avoir vue « Plus tôt »
    Alors je vois le champ « Heure à laquelle tu l'as vue »
    Quand j'indique l'heure 2026-10-05T19:05
    Et je choisis la direction « Ouest »
    Et je demande à identifier ma lumière
    Alors Là-haut cherche ce qui était à l'ouest le 5 octobre 2026 à 19:05:00, au-dessus de Paris

  Scénario: La rose des vents propose huit directions autour de moi
    Quand j'ouvre l'adresse #cetait-quoi
    Alors la rose des vents propose, ligne par ligne :
      | gauche          | milieu   | droite        |
      | NO (Nord-ouest) | N (Nord) | NE (Nord-est) |
      | O (Ouest)       | Toi      | E (Est)       |
      | SO (Sud-ouest)  | S (Sud)  | SE (Sud-est)  |
    Et aucune direction n'est choisie
    Et la page rappelle « Repère : le Soleil se lève vers l'est et se couche vers l'ouest. »

  Scénario: Une seule direction à la fois, et la choisir efface l'alerte
    Quand j'ouvre l'adresse #cetait-quoi
    Et je demande à identifier ma lumière
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » m'alerte : « Choisis la direction où tu l'as vue. »
    Et Là-haut n'a rien cherché
    Quand je choisis la direction « Nord »
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » ne m'alerte plus
    Quand je choisis la direction « Sud-est »
    Alors seul « Sud-est » est choisi parmi « Dans quelle direction ? »

  Scénario: L'heure se vérifie après la direction
    Quand j'ouvre l'adresse #cetait-quoi
    Et je dis l'avoir vue « Plus tôt »
    Et je demande à identifier ma lumière
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » m'alerte : « Choisis la direction où tu l'as vue. »
    Quand je choisis la direction « Est »
    Et je demande à identifier ma lumière
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » m'alerte : « Indique l'heure à laquelle tu l'as vue. »
    Et Là-haut n'a rien cherché

  Scénario: Le bouton « Identifier » patiente pendant que Là-haut cherche
    Étant donné que Là-haut met du temps à identifier ma lumière
    Quand j'ouvre l'adresse #cetait-quoi
    Et je choisis la direction « Est »
    Et je demande à identifier ma lumière
    Alors le bouton « Identifier » indique qu'il travaille
    Quand Là-haut répond enfin
    Alors le bouton « Identifier » ne travaille plus

  Plan du scénario: La page dit pourquoi Là-haut n'a pas pu chercher
    Étant donné que <panne>
    Quand j'ouvre l'adresse #cetait-quoi
    Et je choisis la direction « Est »
    Et je demande à identifier ma lumière
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » m'alerte : « <explication> »

    Exemples:
      | panne                                                                            | explication                                                                      |
      | Là-haut ne cherche que parmi les satellites, dont le catalogue est indisponible | Le catalogue des satellites est indisponible pour le moment, réessaie plus tard. |
      | l'hébergeur de Là-haut est en panne                                              | Le ciel est injoignable pour le moment.                                          |
