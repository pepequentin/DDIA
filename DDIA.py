import json
import random
import csv
from sqlite3 import Timestamp
from typing import Any
import numpy as np
import threading
import shutil
import matplotlib.pyplot as plt
import pandas as pd

# Définir les performances des bots et les moments d'achat et de vente
buy_times = []
sell_times = []
balance_history = []

# CSV file set
csv_file="data.csv"

# CSV file data will be stored inside this variable, in order to be used by multiple threads
data = {}

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    i = 0
    for row in reader:
        open_price = float(row[1])
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        data[i] = {'open': open_price, 'high': high, 'low': low, 'close': close}
        i += 1

# Algorithm used by the program, they are chosen randomly
algo_available = [
    "Bollinger Bands",
    "RSI Strategy",
]

# Configuration of the best file
config = []

def set_config(file_path):
    with open(file_path, "r") as f:
        config = json.load(f)
    return config

class BotThread_load_config(threading.Thread):
    def __init__(self, config, file_path):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.config = config
    def run(self):
        bot = Bot()
        bot.load_config(config, self.file_path)
        bot.change_rsi_default_config()
        bot.change_bollinger_default_config()
        bot.run_algo()
        all_bots_from_a_round.append(bot)

class Bot:
    def __init__(self, config_file=None):
        if config_file:
            # Load configuration from file
            self.load_config(config, config_file)
        else:
            # Default configuration
            self.name = "richard" # Default name
            self.starting_balance = 5000
            self.current_balance = self.starting_balance
            self.pourcentage_to_buy = random.uniform(0.1, 0.999)
            self.pourcentage_to_sell = random.uniform(0.1, 0.999)
            self.algo_used = random.sample(algo_available, k=random.randint(1, len(algo_available)))
            self.num_units_bought = 0
            self.interval_rsi = random.randint(8, 16)
            self.upper_rsi = random.uniform(70, 95)
            self.lower_rsi = random.uniform(0, 30)
            self.period = random.randint(10, 20)
            self.num_std = random.randint(0, 100)
            self.error = 0
            self.algo_params = {}
            for algo in self.algo_used:
                if algo == "RSI Strategy":
                    self.algo_params[algo] = {'interval': self.interval_rsi, 'upper': self.upper_rsi, 'lower': self.lower_rsi, "interval_set": 0, "buy_or_not": 0}
                elif algo == "Bollinger Bands":
                    self.algo_params[algo] = {'period': self.period, 'num_std': self.num_std, "buy_or_not": 0}
                else:
                    raise ValueError("Unknown algorithm: {}".format(algo))

            self.efficacity = 0.0
            self.bought_price = None
            self.config_file_path = None
        self.leveraging = 1  # Niveau d'effet de levier par défaut

    def change_rsi_default_config(self):
        self.interval_rsi = random.randint(8, 16)
        self.upper_rsi = random.uniform(70, 100)
        self.lower_rsi = random.uniform(10, 30)
        self.period = random.randint(12, 16)
        self.num_std = random.randint(0, 100)

    def change_bollinger_default_config(self):
        self.period += random.randint(-50, 50)     
        if self.period < 1:
            self.period = 1
        if self.period > 100:
            self.period = 100
        self.num_std += random.randint(-50, 50)
        if self.num_std < 1:
            self.num_std = 1
        if self.num_std > 100:
            self.num_std = 100
        self.pourcentage_to_buy += random.uniform(-0.2, 0.2)
        if self.pourcentage_to_buy < 0.1:
            self.pourcentage_to_buy = 0.1
        if self.pourcentage_to_buy > 1:
            self.pourcentage_to_buy = 1
        self.pourcentage_to_sell += random.uniform(-0.5, 0.5)
        if self.pourcentage_to_sell < 0.1:
            self.pourcentage_to_sell = 0.1
        if self.pourcentage_to_sell > 1:
            self.pourcentage_to_sell = 1

    def buy(self, price, current_timestamp):
        if price == 0:
            return
        max_buy_units = (self.current_balance * self.pourcentage_to_buy * self.leveraging) / price
        if max_buy_units == 0:
            return
        buy_amount = max_buy_units * price
        self.current_balance -= buy_amount
        self.num_units_bought += max_buy_units
        buy_times.append(current_timestamp)
   
    def sell(self, price, sell_all_units, current_timestamp):
        if sell_all_units == 1:
            sell_units = self.num_units_bought
        else:
            sell_units = (self.num_units_bought * self.pourcentage_to_sell)
        if sell_units == 0:
            return
        sell_amount = sell_units * price
        self.current_balance += sell_amount
        self.num_units_bought -= sell_units
        sell_times.append(current_timestamp)
 

    def rsi(self, prices):
        if len(prices) < self.interval_rsi:
            return None

        delta = np.diff(prices)
        gain = delta * 0
        loss = gain.copy()
        gain[delta > 0] = delta[delta > 0]
        loss[delta < 0] = -delta[delta < 0]
        avg_gain = np.zeros_like(prices)
        avg_loss = np.zeros_like(prices)
        avg_gain[self.interval_rsi-1] = np.mean(gain[:self.interval_rsi])
        avg_loss[self.interval_rsi-1] = np.mean(loss[:self.interval_rsi])

        for i in range(self.interval_rsi, len(prices)):
            if i < self.algo_params['RSI Strategy']['interval_set'][0]:
                # Use only available data up to the interval
                avg_gain[i] = (avg_gain[i-1] * (i-1) + gain[i-1]) / i
                avg_loss[i] = (avg_loss[i-1] * (i-1) + loss[i-1]) / i
            else:
                # Use full interval data
                avg_gain[i] = (avg_gain[i-1] * (self.interval_rsi-1) + gain[i-1]) / self.interval_rsi
                avg_loss[i] = (avg_loss[i-1] * (self.interval_rsi-1) + loss[i-1]) / self.interval_rsi
        if avg_loss[len(avg_loss) - 1] == 0:
            return -1
        rs = avg_gain[len(avg_gain) - 1] / (avg_loss[len(avg_loss) - 1])
        rsi = 100 - (100 / (1 + rs))
        return rsi
    

        
    def run_algo(self):
        # Initialize buy_or_not flags
        buy_or_not_rsi = False
        buy_or_not_bb = False
        
        # Initialize interval_set for RSI strategy
        interval_set = []
        # Iterate through each date
        for i, date in enumerate(sorted(data.keys())):
            # RSI Strategy
            if "RSI Strategy" in self.algo_used:
                prices = [data[k]['close'] for k in sorted(data.keys())[:i+1]]
                # Get the RSI interval
                interval = self.interval_rsi
                upper = self.upper_rsi
                lower = self.lower_rsi
                
                n = len(prices)
                rsi_values = np.zeros(n)
                
                if i >= interval - 1:
                    rsi = self.rsi(prices[i-interval+1:i+1])
                    rsi_values[i] = rsi
                    if rsi_values[i] == -1:
                        self.error+=1
                    elif rsi > upper and buy_or_not_rsi:
                        self.buy(prices[i], i)
                        buy_or_not_rsi = False
                    elif rsi < lower and not buy_or_not_rsi:
                        self.sell(prices[i], 0, i)
                        buy_or_not_rsi = True
                else:
                    interval_set.append(prices[i])
                    if len(interval_set) == interval:
                        rsi = self.rsi(interval_set, i)
                        rsi_values[i] = rsi
                        interval_set = []

            # Bollinger Bands Strategy
            if "Bollinger Bands" in self.algo_used:
                # Get the strategy parameters
                period = self.period
                num_std = self.num_std
                
                # Extract the price for the current date and the previous period
                prices = [data[k]["close"] for k in sorted(data.keys())[:i+1][-period:]]
                
                # Calculate the middle Bollinger Band
                middle_band = moving_average(prices, period)
                
                # Calculate the upper and lower Bollinger Bands
                upper_band = middle_band + num_std * standard_deviation(prices, period)
                lower_band = middle_band - num_std * standard_deviation(prices, period)
                
                # Check if the price is above the upper Bollinger Band
                if data[date]["close"] > upper_band[0]:
                    self.sell(data[date]["close"], 0, i)
                    buy_or_not_bb = True
                
                # Check if the price is below the lower Bollinger Band
                elif data[date]["close"] < lower_band[0] and buy_or_not_bb:
                    self.buy(data[date]["close"], i)
                    buy_or_not_bb = False
            
            # Get and store the potential balance of the bot
            potential_balance = self.current_balance + (self.num_units_bought * data[i]['close'] * self.leveraging)
            balance_history.append(potential_balance)
        
        # Sell every remaining unit bought
        self.sell(data[len(data) - 1]["close"], 1, i)

    def load_config(self, config, file_path):
        # Set attributes from config
        self.name = config["name"]
        self.starting_balance = config["starting_balance"]
        self.algo_used = config["algo_used"]
        self.efficacity = config["efficacity"]
        self.interval_rsi = config["interval_rsi"]
        self.upper_rsi = config["upper_rsi"]
        self.lower_rsi = config["lower_rsi"]
        self.period = config["period"]
        self.num_std = config["num_std"]
        self.error = config["error"]
        self.pourcentage_to_buy = config["pourcentage_to_buy"]
        self.pourcentage_to_sell = config["pourcentage_to_sell"]
        self.config_file_path = file_path
        self.algo_params = config["algo_params"]

    def save_config(self, file_path):
        # Get bot attributes
        config = {
            'name': self.name,
            'starting_balance': self.starting_balance,
            'current_balance': self.current_balance,
            'algo_used': self.algo_used,
            'efficacity': self.efficacity,
            'interval_rsi': self.interval_rsi,
            'upper_rsi': self.upper_rsi,
            'lower_rsi': self.lower_rsi,
            'period': self.period,
            'num_std': self.num_std,
            'pourcentage_to_buy': self.pourcentage_to_buy,
            'pourcentage_to_sell': self.pourcentage_to_sell,
            'error': self.error,
            'algo_params': self.algo_params,
            }

        # Write to file in order to save the config
        with open(file_path, 'w') as f:
            json.dump(config, f)


def moving_average(prices, period):
    """
    Calculates the moving average of the prices over a given period.
    """
    return np.convolve(prices, np.ones(period)/period, mode='valid')

def standard_deviation(prices, period):
    """
    Calculates the standard deviation of the prices over a given period.
    """
    return np.std(prices[-period:])

if __name__ == '__main__':

    # Get the best file
    best_file = "bestfile.txt"
    best_balance = 0
    all_bots_from_a_round = []
    new_bot = Bot()

    # Set the config of the best bot in a "DATA" variable in order to be used by threads
    config = set_config(best_file)
    # Load the config in the bot
    new_bot.load_config(config, best_file)
    # Run the algo on the "new_bot" variable
    new_bot.run_algo()

    # Save the best bot in a file
    best_balance = new_bot.current_balance

    # Second round and beyond
    round_num = 1  # Start from round 1

    print("Debut de la simulation")
    while round_num <= 1:  # Change the number of rounds as needed
        buy_times = []
        sell_times = []
        balance_history = []
        config = set_config(best_file) # Load the wanted config file, here: the best one
        all_bots_from_a_round = []
        threads_second_round = []
        print(f'Round {round_num}')
        for i in range(1):
            new_thread = BotThread_load_config(config, best_file)
            threads_second_round.append(new_thread)
            new_thread.start()

        for new_thread in threads_second_round:
            new_thread.join()

        # sort the bots by current balance in descending order
        sorted_bots_by_current_balance = sorted(all_bots_from_a_round, key=lambda x: x.current_balance, reverse=True)
        # print (f'Best from this round: {sorted_bots_by_current_balance[0].current_balance}')
        if sorted_bots_by_current_balance[0].current_balance > best_balance:
            # Save the best bot in a file
            best_bot_current_round = sorted_bots_by_current_balance[0]
            best_bot_current_round.save_config(f'config_file/config_file_{round_num}.txt')
            best_file = f"config_file/config_file_{round_num}.txt"
            best_balance = best_bot_current_round.current_balance
            print(f"Round {round_num}, New best bot: current_balance={best_bot_current_round.current_balance}")
            # Copy into the bestfile.txt config file
            shutil.copy(best_file, "bestfile.txt")

        # Next round
        round_num += 1

    print("Fin de la simulation\n")
    print("Display the performance of the best bot")
    buy_times = []
    sell_times = []
    balance_history = []

    new_bot = Bot()

    # Set the config of the best bot in a "DATA" variable in order to be used by threads
    config = set_config(best_file)
    # Load the config in the bot
    new_bot.load_config(config, best_file)
    # Run the algo on the "new_bot" variable
    new_bot.run_algo()

    # Charger les données du fichier CSV dans un DataFrame pandas
    alldata = pd.read_csv(csv_file)
    fig, ax1 = plt.subplots()

    # Créer un graphique à partir des performances des bots et de la courbe close
    close_prices = alldata['Close']
    ax1.plot(close_prices)

    # Ajouter des marqueurs pour les moments d'achat et de vente
    ax1.scatter(buy_times, close_prices[buy_times], marker='^', color='green', edgecolor='none', s=50)
    ax1.scatter(sell_times, close_prices[sell_times], marker='v', color='red', edgecolor='none', s=50)

    # Ajouter une légende et un titre
    ax1.legend(['Close row ETH', 'Buy times', 'Sell times'])
    ax1.set_title('Bot performance over time')

    # Tracer la courbe de balance
    ax2 = ax1.twinx()
    ax2.plot(balance_history, color='black')
    ax2.set_ylabel('Potential Balance $', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Étendre l'axe des abscisses de ax2
    x1_lim, x2_lim = ax1.get_xlim()
    ax2.set_xlim(x1_lim, x2_lim)
    # Définir le titre de la fenêtre ###### DOESNT WORKS
    plt.title("Bot performance over time")

    # Afficher le graphique
    plt.show()
