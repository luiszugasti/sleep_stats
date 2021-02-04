import pandas as pd
import numpy as np

data = pd.read_csv("data/sleepdata.csv",delimiter=",")
data = data.iloc[:, : 4]

# n x 2 array. Column 1 is days from 1 to n, column 2 is the time slept
size = len(data.index)
first_array = np.empty([size, 2], dtype=int)

i = 0
for elm in data["Time in bed"]:
    s = elm.split(":")
    s = int(s[0]) * 60 + int(s[1])
    first_array[i][0] = i
    first_array[i][1] = s
    i += 1
print(first_array)

# i = 0
# for elm in data["Time in bed"]:
#     s = elm.split(":")
#     elm = int(s[0]) * 60 + int(s[1])

#     first_array.append([i, elm])
#     i += 1