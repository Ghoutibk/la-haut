# language: fr
Fonctionnalité: Signaler un problème ou proposer une idée
  En tant que visiteur de Là-haut
  Je veux écrire à l'auteur du site
  Afin qu'il corrige ce qui ne marche pas et entende mes idées

  Contexte:
    Étant donné une boîte à avis privée sur GitHub

  Scénario: Je signale un problème et laisse mon e-mail pour avoir une réponse
    Quand j'envoie le problème « La boussole ne bouge pas sur mon Android » avec mon e-mail claire@example.org
    Alors un ticket « problème » arrive dans la boîte à avis, avec mon message et mon e-mail

  Scénario: Je propose une idée sans laisser d'e-mail
    Quand j'envoie l'idée « Ajouter les passages de la Lune »
    Alors un ticket « idée » arrive dans la boîte à avis, avec mon message et sans e-mail

  Scénario: Un message vide est refusé
    Quand j'envoie un problème sans message
    Alors mon avis est refusé : « Écris ton message avant de l'envoyer. »
    Et aucun ticket n'arrive dans la boîte à avis

  Scénario: Un message de plus de 2 000 caractères est refusé
    Quand j'envoie un problème de 2001 caractères
    Alors mon avis est refusé : « Ton message dépasse 2000 caractères : raccourcis-le un peu. »
    Et aucun ticket n'arrive dans la boîte à avis

  Scénario: Une adresse e-mail illisible est refusée
    Quand j'envoie le problème « La boussole ne bouge pas sur mon Android » avec mon e-mail claire.example.org
    Alors mon avis est refusé : « Cette adresse e-mail ne semble pas valide. »
    Et aucun ticket n'arrive dans la boîte à avis
