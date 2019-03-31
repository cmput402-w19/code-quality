# Given a .json file, creates a scatterplot of Lines of Code (Test Lines and All Lines) Per Commit

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
y2 = data["total_lines_per_commit"]

fig, ax = plt.subplots()
ax.scatter(x, y, label="Test Lines of Code", s=1)
ax.scatter(x, y2, label="All Lines of Code", s=1)
ax.legend()

ax.set(xlabel="Commit #", ylabel="Lines of Code", title="Change in Lines Per Commit")
ax.grid()
plt.show()
