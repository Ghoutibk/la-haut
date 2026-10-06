# language: fr
Fonctionnalité: Reconnaître un train Starlink
  En tant que curieux qui a vu une file de points lumineux traverser le ciel
  Je veux que les Starlink d'un même lancement soient annoncés comme un seul train
  Afin de savoir que ce n'était pas un OVNI

  Contexte:
    Étant donné un observateur à Paris
    Et un catalogue qui suit trois Starlink d'un même lancement, à quinze secondes l'un de l'autre

  Scénario: Les Starlink d'un même lancement passent en un seul train
    Quand je cherche les passages visibles du 4 juillet 2018 à 3 h au 4 juillet 2018 à 6 h
    Alors je vois un seul passage, un train Starlink de 3 satellites, le 4 juillet 2018 de 04:54 à 04:58

  Scénario: Je reconnais le train Starlink que j'ai vu passer
    Quand j'ai vu une lumière le 4 juillet 2018 à 04:56, direction sud-est
    Alors la lumière était un train Starlink de 3 satellites
