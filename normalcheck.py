# Creates a scatterplot of Test Lines of Code vs Commits For All Repositories
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import describe, normaltest

xData = []
yData = []
repoList = []

fileTypes = ["java", "py", "js"]  # List of all language types to check


class Counter:
    def __init__(self, *args, **kwargs):
        self.total_lines = 0
        self.total_commits = 0
        self.commits_with_tests = 0
        self.source_commits = 0
        self.test_lines = 0

    def get_normality_stats(self, f, json_data, file_data, fileName, file_type):

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
                       # 'head_commit',
                       ]
        fileout = {}
        for value in json_values:
            value_array = []
            for repo in json_data:
                result = repo[value]
                value_array.append(result)

                self.total_lines += repo['total_lines']
                self.total_commits += repo['actual_commits']
                self.commits_with_tests += repo['commits_with_tests']
                self.source_commits += repo['source_commits']
                self.test_lines += repo['test_lines']

            result = str(normaltest(value_array))
            fileout[value] = result
            fig, ax = plt.subplots()
            ax.hist(value_array)
            fileName = fileName.split(".json")[0]

            ax.set(xlabel=value, ylabel="# of occurrences",
                   title="{} Histogram for {}")
            ax.grid()

            plt.savefig('{}.png'.format("./results/descriptive_stats/histogram for " + value + "for " + file_type))
            plt.close()

        file = open("./results/descriptive_stats/normal " + file_type + '.json', 'w')
        file.write(json.dumps(fileout, indent=1))
        file.close()


def main():
    try:
        os.mkdir("./results/descriptive_stats")
    except:
        pass
    s = Counter()
    for file_type in fileTypes:
        allFiles = os.listdir("./results/" + file_type)
        data_list = []
        for f in allFiles:
            fileName = f
            f = "./results/" + file_type + "/" + f
            print(f)
            fp = open(f, "r")
            data = json.load(fp)
            data_list.append(data)
            fp.close()

        s.get_normality_stats(f, data_list, file_type, fileName, file_type)
        f = './results/descriptive_stats/totals {}.json'.format(file_type)
        fp = open(f, 'w')
        fileout = {
            'total_lines': s.total_lines,
            'total_commits': s.total_commits,
            'source_commits': s.source_commits,
            'commits_with_tests': s.commits_with_tests,
            'test_lines': s.test_lines
        }
        fp.write(json.dumps(fileout, indent=1))
        fp.close()


main()