# Given a .json file, creates a double line graph of total lines of Code (Test and All) at each Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

fileTypes = ["java", "python", "javascript"] # List of all language types to check
graphName = "FilesVsCommits" # const
# Used for subfolder name

def makeGraph(f, data, fileType, fileName):
    xData = []
    yData = []
    yData2 = []
    y = 0
    y2 = 0
    for i in range(len(data["number_of_test_files_per_commit"])):
        xData.append(i+1)
        y = y + data["number_of_test_files_per_commit"][i]
        y2 = y2 + data["number_of_files_per_commit"][i]
        yData.append(y)
        yData2.append(y2)
    
    x = xData
    y = yData
    y2 = yData2
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Test Files")
    ax.plot(x, y2, label="All Files")
    ax.legend()
    fileName = fileName.split(".json")[0]   
    ax.set(xlabel="Commit #", ylabel="Total Files", title="Total Files At Each Commit (" + fileName + ")")
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


