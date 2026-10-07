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
