# Creates a scatterplot of Test Lines of Code vs Commits For All Repositories
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import describe

xData = []
yData = []
repoList = []


def get_describe_stats():
    pass


def main():
    os.chdir('results')
    results = ['js', 'java', 'python']
    allFiles = {'js':[], 'java':[], 'python':[]}
    print(os.getcwd())
    for type_res in results:
        os.chdir(type_res)
        allFiles[type_res] = os.listdir(os.getcwd())
        os.chdir('..')
    json_results = []
    os.chdir('python')

    for file_result in allFiles['python']:
        fp  = open(file_result)
        data = json.load(fp)
        fp.close()
        json_results.append({file_result: data})
    
    
    json_values = ['actual_commits',
        'commits_with_tests',
        'source_commits',
        'total_lines',
        'test_lines',
        'number_of_test_files',
        'number_of_total_files',
        # "number_of_test_files_per_commit",
        # "number_of_files_per_commit",
        # 'test_lines_per_commit',
        # 'total_lines_per_commit',
        #'head_commit',
    ]
    fileout = {}
    for value in json_values:
        value_array = []
        for key in json_results:
            name = list(key.keys())[0]
            result = list(key.values())[0]
            value_array.append(result[value])
            if result['test_lines'] < 0:
                print(name)
        result = str(describe(value_array))
        fileout[value] = result
    file = open('../yeet', 'w')
    file.write(json.dumps(fileout, indent=1))
    file.close()

main()