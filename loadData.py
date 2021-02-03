import pandas as pd

data = pd.read_csv("data/sleepdata.csv",delimiter=";")
data = data.iloc[:, : 4]
for elm in data["Time in bed"]:
    s = elm.split(":")
    elm = int(s[0]) * 60 + int(s[1])
    print(elm)
print(data["Time in bed"])
