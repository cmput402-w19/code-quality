# Given a .json file, creates a line graph of Total Test Lines Per Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

fp = open("flask.json", "r")
data = json.load(fp)
fp.close()

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

ax.set(xlabel="Commit #", ylabel="Total Test Related LOC", title="Total Test Lines Per Commit")
ax.grid()
plt.show()
