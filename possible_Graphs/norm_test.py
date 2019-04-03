#from scipy import stats
#from scipy.stats import ks_2samp
import numpy as np
import os
import json
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats



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

for i in range(len(repoList)):
#for i in range(0,1):
    fp = open(os.getcwd()+"/results/js/"+ repoList[i], "r")
    data = json.load(fp)
    fp.close()
    xData.append(data["total_lines"])
    yData.append(data["test_lines"])

x = xData
y = yData

norm_array = np.concatenate((x,y))
k2, p = stats.normaltest(norm_array)

alpha = 1e-3

print("p = {:g}".format(p))
print(p)
print( p < alpha)
