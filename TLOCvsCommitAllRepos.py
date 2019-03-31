# Creates a scatterplot of Test Lines of Code vs Commits For All Repositories
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

xData = []
yData = []
repoList = []
allFiles = os.listdir(os.getcwd())

for f in allFiles:
    if ".json" in f:
        repoList.append(f)

for i in range(len(repoList)):
    fp = open(repoList[i], "r")
    data = json.load(fp)
    fp.close()

    xData.append(data["total_commits"])
    yData.append(data["test_lines"])

x = xData
y = yData

fig, ax = plt.subplots()
ax.scatter(x, y)

ax.set(xlabel="Commits", ylabel="Total Test Related LOC", title="Total Test Lines vs Commits for All Repositories")
ax.grid()
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()
