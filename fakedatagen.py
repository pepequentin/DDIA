import configparser
import string
import random
import re
import codecs

# Generation of the full dataset into memory
cont = 0
dataset = []
header = "Date,Open,High,Low,Close"
timestamp=1
open=1000
high=1010
low=900
close=1002

dataset.append(header)

while cont < 10000:
    # Concaténer les valeurs en une chaîne séparée par des virgules
    result_string = ','.join(map(str, [timestamp, open, high, low, close]))

    dataset.append(result_string)
    timestamp+=1
    open  *= random.uniform(0.95, 1.05)
    high  *= random.uniform(0.95, 1.05)
    low   *= random.uniform(0.95, 1.05)
    close *= random.uniform(0.95, 1.05)

    cont += 1

# Write to file in one single action
with codecs.open("data.csv", "w", encoding="utf-8") as f:
    f.writelines("\n".join(dataset))