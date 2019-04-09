# code-quality
Team 3 - Code Quality Project
Boris Fleysher, Michael Paradis, Justin Widney

In this project, we analyze the amount of tests over time for the top 100 java, python and js repos found on github at this time.

Steps to reproduce our results:

0. You will need python 3.5.2 or later, as well as pip installed.
1. Run `pip install -r requirements.txt` to download pyDriller and all the necessary componenets
2. Clone this repo
3. Run `./getJavaRepos`, `./getJavaScriptRepos` and `./getPythonRepos`. This will clone all the repos into ./repos so that they can be analyzed in the next step.
4. Run `python repoAnalyzer.py`. This will now run through all 300 repos and extract all the data we used for our analysis into the ./results folder. This should take a few days to a week, depending on the strength of your machine.
5. Once you have generated the data, you can run `Proportion.py` and `TotalLinesVsCommits.py` to generate a folder in /results with the same name as the script which will store all the graphs for each repository.
