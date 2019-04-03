#from scipy import stats
#from scipy.stats import ks_2samp
import numpy as np
import os
import json
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats




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

for i in range(0,1):
#for i in range(0,1):
    #fp = open(os.getcwd()+"/results/js/"+ repoList[i], "r")
    fp = open(os.getcwd()+"/results/js/"+ "ember.js.json", "r")
    data = json.load(fp)
    fp.close()
    xData = data["test_lines_per_commit"]
    #yData.append(data["test_lines"])

print(xData)

for x in xData:
    if x!= 0:
        yData.append(x)



x= np.argwhere(xData)
print(x)
#x = xData[xData != 0]
y = yData

plt.plot(y)
plt.show()
