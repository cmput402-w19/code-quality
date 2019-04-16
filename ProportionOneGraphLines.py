# Given a .json file, creates a double line graph of the proportion of Test Files/Lines vs Source at each Commit

import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

fileTypes = ["java", "py", "js"] # List of all language types to check
graphName = "Proportion" # const
# Used for subfolder name

def makeGraph( fileType, i):


    allFiles = os.listdir("./results/" + i)

    fig, ax = plt.subplots()

    for f in allFiles:
        fileName = f
        f = "./results/" + i + "/" + f
        print(f)
        fp = open(f, "r")
        data = json.load(fp)

        if(data["source_commits"] > 10000):
            continue 
            

        fp.close()


        xData = []
        yData = []
        yData2 = []
        y = 0
        y2 = 0
        y3 = 0
        y4 = 0
        for a in range(len(data["number_of_test_files_per_commit"])):
            xData.append(a+1)
            y = y + data["number_of_test_files_per_commit"][a]
            y2 = y2 + data["number_of_files_per_commit"][a]
            if (y+y2) == 0:  # y2 might be zero during division
                yData.append(0)
            else:
                yData.append(float(y)/float(y+y2)*100)
            y3 = y3 + data["test_lines_per_commit"][a]
            y4 = y4 + data["total_lines_per_commit"][a]
            if (y3+y4) == 0:
                yData2.append(0)
            else:
                yData2.append(float(y3)/float(y3+y4)*100) 

        x = xData
        y = yData   # test files per commit
        y2 = yData2 # test lines per commit 
        #ax.plot(x, y)
        ax.plot(x, y2)
    ax.legend()

    fileName = fileName.split(".json")[0]
   
    ax.set(xlabel="Commit #", ylabel="Percentage(%)", title="Percentage of Test Material vs Total Material")
    ax.grid()
    plt.ylim(0, 100)


    try:
        os.mkdir("./results/" + graphName + "/" + fileType)
    except:
        pass
    plt.savefig('{}.png'.format("./results/" + graphName + "/" + fileType + "Lines" ))
    plt.close()




try:
    os.mkdir("./results/" + graphName)
except:
    pass

for i in fileTypes:

    makeGraph(i,i) 

   



