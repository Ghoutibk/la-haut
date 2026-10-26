# language: fr
Fonctionnalité: Écrire à l'auteur depuis la page
  En tant que visiteur de Là-haut
  Je veux ouvrir une fenêtre d'avis depuis n'importe quel onglet
  Afin de signaler un problème ou de proposer une idée sans quitter la page

  Scénario: Le bouton « Avis » de l'en-tête ouvre la fenêtre d'avis
    Quand j'ouvre Là-haut
    Et je touche « Avis » dans l'en-tête
    Alors la fenêtre « Un souci, une idée ? » est ouverte
    Et la fenêtre dit « Dis-nous ce qui ne marche pas ou ce qui te manquerait. Ton message n'est lu que par l'auteur du site. »
    Et la fenêtre dit « Ton e-mail ne sert qu'à te répondre. Il n'est jamais affiché sur le site. »
    Et seul « Un problème » est choisi parmi « C'est plutôt… »

  Scénario: L'ancienne adresse #avis ouvre la fenêtre d'avis par-dessus « Ce soir »
    Quand j'ouvre l'adresse #avis
    Alors la fenêtre « Un souci, une idée ? » est ouverte
    Quand je touche « Fermer »
    Alors je vois la vue « Au-dessus de toi »
    Et l'onglet « Ce soir » est l'onglet actif

  Scénario: L'adresse #avis n'ouvre la fenêtre qu'au chargement de la page
    Quand j'ouvre l'adresse #cetait-quoi
    Et je change l'adresse pour #avis
    Alors la fenêtre « Un souci, une idée ? » est fermée
    Et je vois la vue « Au-dessus de toi »

  Scénario: « Ce n'était pas ça ? » ouvre la fenêtre d'avis depuis la réponse
    Quand j'ouvre l'adresse #cetait-quoi
    Et je choisis la direction « Nord »
    Et je demande à identifier ma lumière
    Et je touche « Ce n'était pas ça ? Dis-le-nous »
    Alors la fenêtre « Un souci, une idée ? » est ouverte

  Scénario: Je signale un problème et laisse mon e-mail
    Quand j'ouvre la fenêtre d'avis
    Et j'écris « La boussole ne bouge pas sur mon Android »
    Et je laisse mon e-mail claire@example.org
    Et j'envoie mon message
    Alors la fenêtre dit « Bien reçu »
    Et la fenêtre s'intitule désormais « Merci ! »
    Et la réponse « Merci ! » est annoncée sans m'interrompre
    Et la fenêtre dit « Ton message est arrivé chez l'auteur du site. Si tu as laissé ton e-mail, il pourra te répondre. »
    Et l'auteur reçoit un problème : « La boussole ne bouge pas sur mon Android », avec l'e-mail claire@example.org

  Plan du scénario: Je dis de quelle nature est mon avis
    Quand j'ouvre la fenêtre d'avis
    Et je choisis « <bouton> » parmi « C'est plutôt… »
    Et j'écris « Ajouter les passages de la Lune »
    Et j'envoie mon message
    Alors l'auteur reçoit <nature> : « Ajouter les passages de la Lune », sans e-mail
    Quand je touche « Écrire un autre message »
    Alors seul « <bouton> » est choisi parmi « C'est plutôt… »

    Exemples:
      | bouton      | nature      |
      | Une idée    | une idée    |
      | Autre chose | autre chose |

  Scénario: Après un envoi, j'écris un autre message sur un formulaire vidé
    Quand j'ouvre la fenêtre d'avis
    Et j'écris « Merci pour le site »
    Et je laisse mon e-mail claire@example.org
    Et j'envoie mon message
    Et je touche « Écrire un autre message »
    Alors la fenêtre ne dit pas « Bien reçu »
    Et le champ « Ton message » est vide
    Et le champ « Ton e-mail, si tu veux une réponse (facultatif) » est vide

  Scénario: Après un merci, la fenêtre se rouvre sur le formulaire
    Quand j'ouvre la fenêtre d'avis
    Et j'écris « Merci pour le site »
    Et j'envoie mon message
    Et je touche « Fermer »
    Et je touche « Avis » dans l'en-tête
    Alors la fenêtre ne dit pas « Bien reçu »
    Et le champ « Ton message » est vide

  Scénario: La fenêtre se rouvre avec mon brouillon, sans l'ancienne alerte
    Quand j'ouvre la fenêtre d'avis
    Et j'envoie mon message
    Alors la fenêtre m'alerte : « Écris ton message avant de l'envoyer. »
    Quand j'écris « Une idée en cours »
    Et je touche « Fermer »
    Et je touche « Avis » dans l'en-tête
    Alors la fenêtre ne m'alerte plus
    Et le champ « Ton message » contient « Une idée en cours »

  Scénario: Un message fait d'espaces ne part pas
    Quand j'ouvre la fenêtre d'avis
    Et j'écris «    »
    Et j'envoie mon message
    Alors la fenêtre m'alerte : « Écris ton message avant de l'envoyer. »
    Et l'auteur ne reçoit rien

  Scénario: Un message tient en 2 000 caractères, une adresse en 254
    Quand j'ouvre la fenêtre d'avis
    Et j'écris un message de 2001 caractères
    Et je laisse une adresse de 255 caractères
    Alors le champ « Ton message » garde 2000 caractères
    Et le champ « Ton e-mail, si tu veux une réponse (facultatif) » garde 254 caractères

  Scénario: Le bouton « Envoyer » patiente pendant l'envoi
    Étant donné que Là-haut met du temps à recevoir mon message
    Quand j'ouvre la fenêtre d'avis
    Et j'écris « La boussole ne bouge pas »
    Et j'envoie mon message
    Alors le bouton « Envoyer » indique qu'il travaille
    Quand Là-haut répond enfin
    Alors la fenêtre dit « Bien reçu »
    Quand je touche « Écrire un autre message »
    Alors le bouton « Envoyer » ne travaille plus

  Plan du scénario: La fenêtre dit pourquoi mon message n'est pas parti, et le garde
    Étant donné que <empêchement>
    Quand j'ouvre la fenêtre d'avis
    Et j'écris « La boussole ne bouge pas »
    Et je laisse mon e-mail <e-mail>
    Et j'envoie mon message
    Alors la fenêtre m'alerte : « <explication> »
    Et le champ « Ton message » contient « La boussole ne bouge pas »

    Exemples:
      | empêchement                                         | e-mail             | explication                                                           |
      | la boîte à avis est prête                           | claire@            | Cette adresse e-mail ne semble pas valide.                            |
      | Là-haut a déjà reçu trop de messages cette heure-ci | claire@example.org | Beaucoup de messages viennent d'arriver : réessaie dans un moment.    |
      | la boîte à avis est injoignable                     | claire@example.org | L'envoi des avis est indisponible pour le moment, réessaie plus tard. |
      | l'hébergeur de Là-haut est en panne                 | claire@example.org | Ton message n'a pas pu partir : vérifie-le et réessaie.               |

  Scénario: Le piège à robots reste hors de vue, et un robot qui le remplit croit avoir réussi
    Quand j'ouvre la fenêtre d'avis
    Alors le champ « Ne remplis pas ce champ » est hors de l'écran et caché aux lecteurs d'écran
    Et le clavier passe du champ « Ton e-mail, si tu veux une réponse (facultatif) » au bouton « Envoyer »
    Quand un robot remplit le champ « Ne remplis pas ce champ » avec « https://spam.example »
    Et j'écris « Gagnez des bitcoins »
    Et j'envoie mon message
    Alors la fenêtre dit « Bien reçu »
    Et l'auteur ne reçoit rien

  Plan du scénario: Je ferme la fenêtre d'avis
    Quand j'ouvre la fenêtre d'avis
    Et <geste>
    Alors la fenêtre « Un souci, une idée ? » est fermée

    Exemples:
      | geste                                          |
      | je touche « Fermer »                           |
      | j'appuie sur Échap                             |
      | je touche le fond assombri, hors de la fenêtre |

  Scénario: Toucher la fenêtre elle-même ou valider au clavier ne la ferme pas
    Quand j'ouvre la fenêtre d'avis
    Et je touche la fenêtre, hors de ses boutons et de ses champs
    Alors la fenêtre « Un souci, une idée ? » est ouverte
    Quand je valide au clavier depuis le champ « Ton e-mail, si tu veux une réponse (facultatif) »
    Alors la fenêtre m'alerte : « Écris ton message avant de l'envoyer. »
    Et la fenêtre « Un souci, une idée ? » est ouverte
