# README

## Aperçu

Ce script Python simule un bot de trading utilisant deux stratégies différentes, à savoir les "Bollinger Bands" et la "Stratégie RSI". Le comportement du bot est simulé sur des données historiques de prix provenant d'un fichier CSV contenant les prix de la cryptomonnaie. Le script inclut également le multi-threading pour simuler plusieurs instances du bot avec différentes configurations.

## Prérequis

Avant d'exécuter le script, assurez-vous d'avoir installé les packages Python nécessaires. Vous pouvez les installer à l'aide de la commande suivante :

```bash
pip install numpy matplotlib pandas
```

## Utilisation

1. **Données CSV**

   Assurez-vous d'avoir un fichier CSV nommé "data.csv" contenant des données historiques de prix. Le fichier CSV doit avoir des colonnes pour 'Open', 'High', 'Low' et 'Close'.

2. **Configuration**

   Le script utilise un fichier de configuration nommé "bestfile.txt" pour stocker les paramètres du bot le mieux performant. S'il n'existe pas, le script le créera pendant la simulation.

3. **Exécuter le script**

   Exécutez le script à l'aide de la commande suivante :

   ```bash
   python DDIA.py
   ```

4. **Sortie de la simulation**

   Le script simule plusieurs rounds, optimisant la configuration du bot en fonction de la configuration la mieux performante à chaque tour. Le script affiche des informations sur chaque round et met à jour le fichier de configuration "bestfile.txt" en conséquence.

## Format du fichier de configuration

Le fichier de configuration "bestfile.txt" stocke les paramètres du bot le mieux performant. Le fichier est au format JSON et comprend les paramètres suivants (possible de custom):

- `name` : Nom du bot.
- `starting_balance` : Solde initial du bot.
- `current_balance` : Solde actuel du bot.
- `algo_used` : Liste des stratégies utilisées par le bot.
- `efficacity` : Efficacité du bot.
- `interval_rsi` : Intervalle RSI pour la stratégie.
- `upper_rsi` : Seuil RSI supérieur.
- `lower_rsi` : Seuil RSI inférieur.
- `period` : Période pour la stratégie des Bollinger Bands.
- `num_std` : Nombre d'écart-types pour les Bollinger Bands.
- `pourcentage_to_buy` : Pourcentage du solde à utiliser pour l'achat.
- `pourcentage_to_sell` : Pourcentage des unités détenues à vendre.
- `error` : Nombre d'erreurs rencontrées lors de la simulation.
- `algo_params` : Paramètres spécifiques à chaque stratégie employée.

## Visualisation

Le script génère un graphique affichant les prix historiques de la cryptomonnaie ainsi que des marqueurs indiquant les moments d'achat et de vente du bot. De plus, il inclut un axe des y secondaire montrant le solde potentiel du bot au fil du temps.

## Remarques

- Le script utilise le multi-threading pour simuler plusieurs instances du bot avec différentes configurations simultanément. Le bot le mieux performant de chaque round est enregistré dans "bestfile.txt" pour les rounds suivants.
- Le script fourni est une simulation et n'est pas destiné au trading en direct. Faites preuve de prudence et effectuez des tests approfondis avant de déployer un algorithme de trading dans un scénario réel.

## Licence

  Le code est open source, faites en bonne usage. Seul nos meilleurs jedis pourront obtenir la satisfaction recherchée.
