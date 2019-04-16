import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

fileTypes = ["java", "py", "js"] # List of all language types to check
graphName = "total_average" # const
# Used for subfolder name
average_array_total = []

def average_for_file_type(data,fileType):

    repos_at_each_commit = []
    max_commits = 0
    proportion_arrays = []
    # Will create an array of the form 
    # [[R1C1, R1C2,...,R1CN],[R2C1, ... R2CM]]
    for repo in data:
        proportion_array = []
        test_lines = 0
        source_lines = 0
        if len(repo['test_lines_per_commit']) > max_commits:
            max_commits = len(repo['test_lines_per_commit'])
        for commit in range(len(repo['test_lines_per_commit'])):
            test_lines += repo["test_lines_per_commit"][commit]
            source_lines += repo["total_lines_per_commit"][commit]
        
            try:
                proportion_array.append(test_lines/source_lines)
            except:
                proportion_array.append(0)
                continue
        proportion_arrays.append(proportion_array)
    
    
    array_of_proportions_for_all_commit = []
    # Will transform the above array into 
    # [[R1C1, R2C1, ... RNC1], [R1C2, ...]]
    for commit in range(max_commits):
        array_of_proportions_at_current_commit = []
        test_lines_at_commit = 0
        total_lines_at_commit = 0
        for repo in proportion_arrays:
            try:
                # Bound checking that is awful
                e = repo[commit]
            except:
                continue
            array_of_proportions_at_current_commit.append(repo[commit])
        array_of_proportions_for_all_commit.append(array_of_proportions_at_current_commit)

    x_array = [] 
    commit_count = 1
    average_array = []
    for commit in array_of_proportions_for_all_commit:
        if len(commit) == 0:
            continue
        average_array.append(sum(commit)/len(commit)*100)
        x_array.append(commit_count)
        commit_count += 1
    x = x_array
    y = average_array
    
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Average of proportion of test code for {} repo".format(fileType))
    ax.legend()
    
    plt.ylim(0, 100)   
    ax.set(xlabel="Commit #", ylabel="Proportion of test code", title="Average proportion of test code for {} repos".format(fileType))
    ax.grid()
    plt.savefig('{}.png'.format("./results/" + graphName + "/" + fileType))
    plt.close()




try:
    os.mkdir("./results/total_average/")
except:
    pass

for i in fileTypes:
    allFiles = os.listdir("./results/" + i)
    file_type_results = []
    for f in allFiles:
        fileName = f
        f = "./results/" + i + "/" + f
        print(f)
        fp = open(f, "r")
        data = json.load(fp)
        file_type_results.append(data)
        fp.close()

    average_for_file_type(file_type_results,i)


