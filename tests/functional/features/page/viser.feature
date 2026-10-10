# language: fr
Fonctionnalité: Viser avec mon téléphone pour donner la direction
  En tant que curieux qui ne connaît pas les points cardinaux
  Je veux pointer mon téléphone vers l'endroit où j'ai vu la lumière
  Afin que la direction se choisisse toute seule

  Contexte:
    Étant donné que nous sommes le 5 octobre 2026 à 21:30

  Scénario: Sur un téléphone avec boussole, Là-haut propose de viser
    Étant donné que je visite Là-haut sur un téléphone Android
    Quand j'ouvre l'adresse #cetait-quoi
    Alors je vois le bouton « Viser avec mon téléphone »
    Et la page dit « Ou choisis la direction toi-même : »

  Plan du scénario: Sans boussole ou sans écran tactile, je choisis la direction moi-même
    Étant donné que je visite Là-haut <appareil>
    Quand j'ouvre l'adresse #cetait-quoi
    Alors je ne vois pas le bouton « Viser avec mon téléphone »
    Et la page ne dit pas « Ou choisis la direction toi-même : »

    Exemples:
      | appareil                       |
      | sur un ordinateur              |
      | sur un téléphone sans boussole |

  Scénario: Sur Android, la rose des vents suit mon téléphone jusqu'à « C'est là »
    Étant donné que je visite Là-haut sur un téléphone Android
    Quand j'ouvre l'adresse #cetait-quoi
    Et je touche « Viser avec mon téléphone »
    Alors la page dit « Tiens ton téléphone à plat devant toi et tourne-toi : le haut de l'écran doit pointer vers l'endroit où tu as vu la lumière. »
    Et la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Lecture de la boussole… »
    Et je ne vois pas le bouton « Viser avec mon téléphone »
    Quand mon téléphone pointe vers 22.4°
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Tu vises le nord »
    Et seul « Nord » est choisi parmi « Dans quelle direction ? »
    Quand mon téléphone pointe vers 22.5°
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Tu vises le nord-est »
    Et seul « Nord-est » est choisi parmi « Dans quelle direction ? »
    Quand 3 secondes passent
    Et mon téléphone pointe vers 90°
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Tu vises l'est »
    Et la vue « Tu as vu une lumière bouger dans le ciel ? » ne m'alerte plus
    Quand je touche « C'est là »
    Alors je vois le bouton « Viser avec mon téléphone »
    Et la page ne dit pas « Tu vises l'est »
    Quand mon téléphone pointe vers 200°
    Alors seul « Est » est choisi parmi « Dans quelle direction ? »

  Scénario: Sans orientation absolue, Android donne le nord par l'orientation ordinaire
    Étant donné que je visite Là-haut sur un téléphone Android sans orientation absolue
    Quand j'ouvre l'adresse #cetait-quoi
    Et je touche « Viser avec mon téléphone »
    Et mon téléphone pointe vers 200°
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Tu vises le sud »
    Et seul « Sud » est choisi parmi « Dans quelle direction ? »

  Scénario: Une boussole qui ne sait pas où est le nord est abandonnée au bout de 3 secondes
    Étant donné que je visite Là-haut sur un téléphone Android sans orientation absolue
    Quand j'ouvre l'adresse #cetait-quoi
    Et je touche « Viser avec mon téléphone »
    Et ma boussole ne sait pas où est le nord
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Lecture de la boussole… »
    Et aucune direction n'est choisie
    Quand 3 secondes passent
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » m'alerte : « La boussole de ton téléphone ne répond pas : choisis la direction toi-même. »
    Et je vois le bouton « Viser avec mon téléphone »
    Quand je choisis la direction « Sud »
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » ne m'alerte plus

  Scénario: Sur iPhone, Là-haut demande l'accès à la boussole quand je touche « Viser »
    Étant donné que je visite Là-haut sur un iPhone, et que j'autorise l'accès à la boussole
    Quand j'ouvre l'adresse #cetait-quoi
    Alors mon iPhone ne m'a pas encore demandé l'accès à la boussole
    Quand je touche « Viser avec mon téléphone »
    Alors mon iPhone m'a demandé l'accès à la boussole
    Quand ma boussole ne sait pas où est le nord
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Lecture de la boussole… »
    Quand mon téléphone pointe vers 135°
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » annonce « Tu vises le sud-est »
    Et seul « Sud-est » est choisi parmi « Dans quelle direction ? »

  Plan du scénario: Sans accès à la boussole de l'iPhone, je choisis la direction moi-même
    Étant donné que je visite Là-haut sur un iPhone, et que <accès>
    Quand j'ouvre l'adresse #cetait-quoi
    Et je touche « Viser avec mon téléphone »
    Alors la vue « Tu as vu une lumière bouger dans le ciel ? » m'alerte : « Sans accès à la boussole, choisis la direction toi-même. »
    Et je vois le bouton « Viser avec mon téléphone »
    Et la page ne dit pas « Lecture de la boussole… »

    Exemples:
      | accès                                   |
      | je refuse l'accès à la boussole         |
      | la demande d'accès à la boussole échoue |

  Scénario: Choisir une direction à la main arrête la visée
    Étant donné que je visite Là-haut sur un téléphone Android
    Quand j'ouvre l'adresse #cetait-quoi
    Et je touche « Viser avec mon téléphone »
    Et mon téléphone pointe vers 47°
    Et je choisis la direction « Sud »
    Alors je vois le bouton « Viser avec mon téléphone »
    Et seul « Sud » est choisi parmi « Dans quelle direction ? »
    Quand mon téléphone pointe vers 90°
    Alors seul « Sud » est choisi parmi « Dans quelle direction ? »

  Scénario: Demander à identifier arrête la visée
    Étant donné que je visite Là-haut sur un téléphone Android
    Quand j'ouvre l'adresse #cetait-quoi
    Et je touche « Viser avec mon téléphone »
    Et mon téléphone pointe vers 47°
    Et je demande à identifier ma lumière
    Alors je vois le bouton « Viser avec mon téléphone »
    Et Là-haut cherche ce qui était au nord-est le 5 octobre 2026 à 21:30:00, au-dessus de Paris
