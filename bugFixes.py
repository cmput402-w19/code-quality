import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os


fileTypes = ["java", "py", "js"] # List of all language types to check

total_fixes = 0
total_fixes_with_tests = 0

for i in fileTypes:
    allFiles = os.listdir("./results/" + i)
    total_fixes = 0
    total_fixes_with_tests = 0
    for f in allFiles:
        fileName = f
        f = "./results/" + i + "/" + f
        fp = open(f, "r")
        data = json.load(fp)
        total_fixes_with_tests = total_fixes_with_tests + data["fixes_with_tests"]
        total_fixes = total_fixes + data["total_fixes"]

        fp.close()
    print(i)
    print(total_fixes_with_tests, "total fixes with tests")
    print(total_fixes, "total fixes")
    print(total_fixes_with_tests/total_fixes, "% of fixes")
    print("\n\n")


