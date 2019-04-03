#from scipy import stats
from scipy.stats import ks_2samp
import numpy as np
import os
import json
import matplotlib
import matplotlib.pyplot as plt



xData = []
yData = []
repoList = []


allFilesJava = os.listdir(os.getcwd()+"/results/java")
allFilesPython = os.listdir(os.getcwd()+"/results/python")
allFilesJs = os.listdir(os.getcwd()+"/results/js")


print(allFilesJs)

for f in allFilesJs:
    if ".json" in f:
        repoList.append(f)

print(repoList)

#for i in range(len(repoList)):
for i in range(0,len(repoList)):
    fp = open(os.getcwd()+"/results/js/"+ repoList[i], "r")
    data = json.load(fp)
    fp.close()
    xData.append(data["total_lines"])

    yData.append(data["test_lines"])

x = xData
y = yData

fig, ax = plt.subplots()
ax.scatter(x, y)

ax.set(xlabel="total_lines", ylabel="test_lines", title="Commits With Tests vs Commits for All Repositories")
ax.grid()
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()
