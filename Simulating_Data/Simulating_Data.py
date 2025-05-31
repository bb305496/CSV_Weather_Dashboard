import numpy as np
from numpy import random
import pandas as pd

# Number of samples
n = 90
random.seed(7)
# Random data generator

# N days
day = np.arange(1, n+1)
# Temperature range (-15,34)
temperature = random.randint(-15, 35, n)
# Precipitation range (0,24)
precipitation = random.uniform(0, 25, n).round(decimals=1)
# Wind range (0,14)
wind = random.uniform(0, 15, n).round(decimals=1)

# Creating data frame for pandas
data = {
    "Day" : day,
    "Temperature[C]": temperature,
    "Precipitation" : precipitation,
    "Wind" : wind
}

df = pd.DataFrame(data)

# Saving data to csv, using ";" as a separator for the Polish version of Excel
# Remove sep="," for English version
df.to_csv("../Data/Weather_data.csv", index=False, sep=";")


