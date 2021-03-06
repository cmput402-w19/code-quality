# Given a .json file, creates a double line graph of the proportion of Test Files/Lines vs Source at each Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

fileTypes = ["java", "py", "js"] # List of all language types to check
graphName = "Proportion" # const
# Used for subfolder name

def makeGraph(f, data, fileType, fileName):
    xData = []
    yData = []
    yData2 = []
    y = 0
    y2 = 0
    y3 = 0
    y4 = 0
    for i in range(len(data["number_of_test_files_per_commit"])):
        xData.append(i+1)
        y = y + data["number_of_test_files_per_commit"][i]
        y2 = y2 + data["number_of_files_per_commit"][i]
        if (y+y2) == 0:  # y2 might be zero during division
            yData.append(0)
        else:
            yData.append(float(y)/float(y+y2)*100)
        y3 = y3 + data["test_lines_per_commit"][i]
        y4 = y4 + data["total_lines_per_commit"][i]
        if (y3+y4) == 0:
            yData2.append(0)
        else:
            yData2.append(float(y3)/float(y3+y4)*100) 

    x = xData
    y = yData   # test files per commit
    y2 = yData2 # test lines per commit 
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Files")
    ax.plot(x, y2, label="Lines")
    ax.legend()

    fileName = fileName.split(".json")[0]
   
    ax.set(xlabel="Commit #", ylabel="Percentage(%)", title="Percentage of Test Material vs Total (" + (fileName) + ")")
    ax.grid()
    plt.ylim(0, 100)


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


