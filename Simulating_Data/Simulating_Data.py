import numpy as np
from numpy import random
import pandas as pd

#Number of samples
n = 1000
random.seed(7)
#Random data generator
day = np.arange(1, n+1)
temperature = random.randint(-15, 35, n)
precipitation = random.uniform(0, 25, n).round(decimals=1)
wind = random.uniform(0, 15, n).round(decimals=1)

#Creating data frame for pandas
data = {
    "Day" : day,
    "Temperature": temperature,
    "Precipitation" : precipitation,
    "Wind" : wind
}

df = pd.DataFrame(data)

#Saving data to csv, using ";" as a separator for the Polish version of Excel
#Remove sep="," for English version
df.to_csv("../Data/Weather_data.csv", index=False, sep=";")


