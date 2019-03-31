# Given a .json file, creates a scatterplot of Test Lines Per Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

fp = open("flask.json", "r")
data = json.load(fp)
fp.close()

xData = []
for i in range(len(data["test_lines_per_commit"])):
    xData.append(i+1)

x = xData
y = data["test_lines_per_commit"]

fig, ax = plt.subplots()
ax.scatter(x, y)

ax.set(xlabel="Commit #", ylabel="Test Related LOC", title="Test Lines Per Commit")
ax.grid()
plt.show()
