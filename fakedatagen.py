import random
import codecs

# Generation of the full dataset into memory
cont = 0
dataset = []
header = "Date,Open,High,Low,Close"
timestamp = 1
open_price = 9000
high_price = 9010
low_price = 8900
close_price = 9002

dataset.append(header)

while cont < 10000:
    # Concatenate values into a string separated by commas
    result_string = ','.join(map(str, [timestamp, open_price, high_price, low_price, close_price]))

    dataset.append(result_string)
    
    # Update values with random variations
    timestamp += 1
    open_price *= random.uniform(0.98, 1.02)
    high_price *= random.uniform(0.98, 1.02)
    low_price *= random.uniform(0.98, 1.02)
    close_price *= random.uniform(0.98, 1.02)

    cont += 1

# Write to file in one single action
with codecs.open("data.csv", "w", encoding="utf-8") as f:
    f.writelines("\n".join(dataset))
