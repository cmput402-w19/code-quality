# Gets the commit hash used for the results in the results/js,py and java folders
# Ouputs a json with each of them in a single json file in results
from repoAnalyzer2 import extractRepoName
import json

def main():
    print('Working on javaScriptRepos')
    reposFile = open('javaScriptRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()
    js_repos = []
    for repo in repoURLs:
        name = extractRepoName(repo)
        fp = open('./results/js/'+name+'.json', "r")
        data = json.load(fp)
        fp.close()
        js_repos.append({repo.strip(): data["head_commit"]})

    print("Working on python")
    reposFile = open('pythonrepolist.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()
    py_repos = []
    for repo in repoURLs:
        name = extractRepoName(repo)
        fp = open('./results/py/'+name+'.json', "r")
        data = json.load(fp)
        fp.close()
        py_repos.append({repo.strip(): data["head_commit"]})

    print('Working on Java')
    reposFile = open('javaRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()
    java_repos = []
    for repo in repoURLs:
        name = extractRepoName(repo)
        fp = open('./results/java/'+name+'.json', "r")
        data = json.load(fp)
        fp.close()
        java_repos.append({repo.strip(): data["head_commit"]})

    file_out = {
        'js_repos' : js_repos,
        'java_repos': java_repos,
        'python_repos': py_repos
    }
    outfile = open('./results/hashs.json', 'w')
    outfile.write(json.dumps(file_out, indent=1))
    outfile.close()

if __name__ == '__main__':
    main()