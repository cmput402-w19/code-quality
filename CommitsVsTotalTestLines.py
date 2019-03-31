import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

fp = open("retrofit.json", "r")
data = json.load(fp)
fp.close()

for i in data:
    print(i)

xData = []
yData = []
y = 0
for i in range(len(data["test_lines_per_commit"])):
    xData.append(i+1)
    y = y + data["test_lines_per_commit"][i]
    yData.append(y)

x = xData
y = yData

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set(xlabel="commits", ylabel="Test related LOC", title="Test lines over commits")
ax.grid()
plt.show()
