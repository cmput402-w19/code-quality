# code-quality
Team 3 - Code Quality Project
Boris Fleysher, Michael Paradis, Justin Widney

In this project, we analyze the amount of tests over time for the top 100 java, python and js repos found on github at this time.

Steps to reproduce our results:

0. You will need python 3.5.2 or later, as well as pip installed and virtualenv. You will also need to be using Ubuntu
1. Clone this repo
   * Create a virtual environment using `virtualenv venv --python=python3` 
   * Activate the virtual environment using `source venv/bin/activate`
   * Run `mkdir repos` to create the folder for the repos.
   * Delete the current results files in `results/js`, `results/py` and `results/java`
2. Run `pip install -r requirements.txt` to download pyDriller and all the necessary componenets
3. Run `sh getJavaRepos.sh`, `sh getJavaScriptRepos.sh` and `sh getPythonRepos.sh`. This will clone all the repos into ./repos so that they can be analyzed in the next step.
4. Run `python repoAnalyzer2.py`. This will now run through all 300 repos and extract all the data we used for our analysis into the ./results folder. This should take a few days to a week, depending on the strength of your machine.   
5. Once you have generated the data, you can run `python Proportion.py` and `pythonTotalLinesVsCommits.py` to generate a folder in /results with the same name as the script which will store all the graphs for each repository.
6. To get the statistics surrounding the inclusion of tests with the completion of features or bug fixes run `python bugFixesStats.py`
7. To get the average proportion per language over time graph run `python average_per_language.py`
8. To get the combined graphs for the languages over time run `python ProportionOneGraphLines.py` the results will be in `results/Proportion/{repo_type}Lines.png
9. To see individual repos proportion graph over time run `python proportionalgraph.py` and see the results in `results/Proportion\ of\ test\ lines/{repo_type}`

## Running for one repo

Since it can take a very long time to get the results we created a file that allows you to get the results for one repo. You can go to `results/hashes.json` to see the repos and what was the hash we used for the analysis. To generate this file run `python get_used_hashes.py`. This needs all results in the results folder to work. Once you have selected a repo from the file along with the hash do the following steps:

1. Delete the results file for the repo by deleting the results file at `results/{repo_type}/{repo_name}.json`
2. Clone the repo into the repos folder if you haven't already.
3. Run `python analyze_one_repo_to_commit.py` and enter the correct values.
4. Wait and feel free to open the file and see the results.

