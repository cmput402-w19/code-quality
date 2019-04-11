# Given a .json file, creates a double line graph of total lines of Code (Test and All) at each Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

fileTypes = [".java", ".py", ".js"] # List of all language types to check
graphName = "Proportion of test lines" # const
# Used for subfolder name

def makeGraph(f, data, fileType, fileName):
    xData = []
    yData = []
    yData2 = []
    y_actual = []
    y = 0
    y2 = 0
    for i in range(len(data["test_lines_per_commit"])):
        xData.append(i+1)
        y = y + data["test_lines_per_commit"][i]
        y2 = y2 + data["total_lines_per_commit"][i]
        yData.append(y)
        yData2.append(y2)
        try:
            y_actual.append(y/y2)
        except:
            return
    
    x = xData
    y = yData
    y2 = yData2
    
    fig, ax = plt.subplots()
    ax.plot(x, y_actual, label="Proportion of test lines of code")
    ax.legend()
    
    fileName = fileName.split(".json")[0]
   
    ax.set(xlabel="Commit #", ylabel="Proportion of test lines", title="Proportion of test lines of code (" + fileName+")")
    ax.grid()

    try:
        os.mkdir("./results/" + graphName + "/" + fileType)
    except:
        pass
    plt.savefig('{}.png'.format("./results/" + graphName + "/" + fileType + "/" + fileName))
    plt.close()




try:
    os.mkdir("./results/" + graphName)
except:
    pass

for i in fileTypes:
    allFiles = os.listdir("./results/" + i)
    for f in allFiles:
        fileName = f
        f = "./results/" + i + "/" + f
        print(f)
        fp = open(f, "r")
        data = json.load(fp)
        fp.close()

        makeGraph(f, data, i, fileName) 


