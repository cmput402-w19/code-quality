# BugFixesStats.py 
# expects json files in ./results/language/filename
# Goes through the json data and outputs a cumulative sum of total bug fixes, compared to the total bug fixes with tests. 


import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os


fileTypes = ["java", "py", "js"] # List of all language types to check

total_fixes = 0
total_fixes_with_tests = 0
all_results = []
for i in fileTypes:
    allFiles = os.listdir("./results/" + i)
    total_fixes = 0
    total_fixes_with_tests = 0
    file_type_results = []
    for f in allFiles:
        fileName = f
        f = "./results/" + i + "/" + f
        fp = open(f, "r")
        data = json.load(fp)
        total_fixes_with_tests = total_fixes_with_tests + data["fixes_with_tests"]
        total_fixes = total_fixes + data["total_fixes"]
        try:
            file_type_results.append(total_fixes_with_tests/total_fixes)
        except:
            pass

        fp.close()
    all_results.append(file_type_results)

    print(i)
    print(total_fixes_with_tests, "total fixes with tests")
    print(total_fixes, "total fixes")
    print(total_fixes_with_tests/total_fixes, "% of fixes")
    print("\n\n")

print(stats.kruskal(all_results[0], all_results[1], all_results[2]))

