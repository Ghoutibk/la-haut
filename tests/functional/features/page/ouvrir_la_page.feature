# language: fr
Fonctionnalité: Ouvrir Là-haut dans mon navigateur
  En tant que curieux qui lève les yeux le soir
  Je veux que la page de Là-haut se présente en français et tienne sur mon téléphone
  Afin de la retrouver et de la lire sans effort

  Scénario: La page se présente en français, aux couleurs de la nuit
    Quand j'ouvre Là-haut
    Alors l'onglet du navigateur s'intitule « Là-haut »
    Et la page est écrite en français
    Et la page se décrit ainsi : « Les satellites visibles ce soir au-dessus de chez toi, et la réponse à « c'était quoi, cette lumière ? ». »
    Et la barre du navigateur prend la couleur de la nuit, #07090F
    Et la page s'étend jusqu'aux bords de l'écran

  Scénario: Les scripts et les styles viennent de Là-haut, seules les polices viennent de Google
    Quand j'ouvre Là-haut
    Alors chaque script et chaque feuille de style vient de Là-haut, sous /static
    Et chaque script est servi comme du JavaScript
    Et la page demande ses polices à Google Fonts, et rien d'autre hors de Là-haut
