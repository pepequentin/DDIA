IA project

$ python.exe DDIA.py


Stats du bot en structure:
    -Efficacité:
    -Argent de départ (fix) : u64
    -Argent actuel : u64
    -Capacité:
                -Nombre d'algo utilisé : u64
                -Tableau de ptr vers les algo de trading choisi
                -Tableau u64 vers le numero de position dans le tableau static des algo de trading (fix, va etre pris en compte seulement a la sauvegarde/chargement du bot)


ETAT : [DONE]
1. Avoir une base de donnée csv sur plusieurs mois, les cours du btc, eth

ETAT : [DONE]
2. Commencer a voir comment faire une ia
    a. La techno, python
    b. 4 agents :
        On va commencer par 1, puis 2, puis 4 bots, sauvegarder letat des bots par round
            ETAT : [DONE]
            1er- Createur/Loader -> createur ou loader de fichier de config pour un bot
            ETAT : [DONE]
            2e - Practice        -> round : sur la DB on prend un temps en jours, random, mini 100x ou 300x sur tous le temps de la db par bot
            ETAT : [DONE]
            3e - Correction      -> Faire les stats du round
            ETAT : [DONE]
            4e - Decision        -> Par round le correction va dupliquer le meilleur de la piscine, modifier les stats du bot de maniere random


ETAT : [PENDING]
3. Tableau des algo de trading 

    ETAT : [DONE]
    Quentin:
     -RSI
     -Bollinger Bands

    ETAT : [PENDING]
    Yann   :

4. Ajouter des stats
        ex: pourcentage_to_sell
    (en discuter tout les deux)
    ETAT :  [PENDING]

ETAT : [NOTHING]
5. Binance
    a. Implementer un acces api a binance
    b. Chopper les données des cours de la crypto voulu et tester en fictif
    c. Tester avec de la vraie

