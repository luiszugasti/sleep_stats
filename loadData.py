import pandas as pd

data = pd.read_csv("data/sleepdata.csv",delimiter=";")
data = data.iloc[:, : 4]
