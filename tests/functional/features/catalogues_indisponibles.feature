# language: fr
Fonctionnalité: Continuer d'annoncer « Ce soir » quand la source des catalogues flanche
  En tant que curieux qui lève les yeux le soir
  Je veux que Là-haut tienne bon quand CelesTrak répond mal ou ne répond plus
  Afin d'avoir quand même les passages, ou au moins un message clair

  Contexte:
    Étant donné un observateur à Paris

  Scénario: Sans aucun catalogue, « Ce soir » demande de réessayer plus tard
    Étant donné Là-haut n'a jamais pu joindre CelesTrak
    Quand j'ouvre « Ce soir » le 7 octobre 2026 à 6 h
    Alors « Ce soir » répond « Le catalogue des satellites est indisponible pour le moment, réessaie plus tard. »

  Scénario: Un groupe injoignable n'empêche pas d'annoncer l'autre
    Étant donné CelesTrak publie ses catalogues du 6 octobre 2026 au format OMM
    Mais le groupe « last-30-days » est injoignable
    Quand j'ouvre « Ce soir » le 7 octobre 2026 à 6 h
    Alors « Ce soir » annonce « Station spatiale chinoise Tiangong » le 7 octobre 2026 de 06:41 à 06:45
    Et « Ce soir » n'annonce aucun Starlink

  Plan du scénario: Le dernier catalogue connu sert quand CelesTrak répond mal
    Étant donné Là-haut a gardé les catalogues du 6 octobre 2026, téléchargés il y a trois heures
    Et CelesTrak <panne>
    Quand j'ouvre « Ce soir » le 7 octobre 2026 à 6 h
    Alors « Ce soir » annonce « Station spatiale chinoise Tiangong » le 7 octobre 2026 de 06:41 à 06:45
    Et « Ce soir » annonce « STARLINK-38375 » le 7 octobre 2026 de 06:16 à 06:19

    Exemples:
      | panne                                           |
      | répond une erreur 503                           |
      | répond une page web au lieu du catalogue        |
      | répond une page web d'une seule ligne démesurée |
      | envoie un catalogue coupé au milieu d'une ligne |
      | interrompt sa réponse en cours de route         |
