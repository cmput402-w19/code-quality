from pydriller import RepositoryMining, GitRepository
import json
import os
from scipy import stats


fileTypes = ["java", "py", "js"] # List of all language types to check
graphName = "first10summary" # const


def extractRepoName(url):
    url = url.split(".git")[0]
    url = url.split("/")[-1]
    return url

class RepoStats2:
    def __init__(self, *args, **kwargs):
        self.repo = None
        self.has_test = False
        return super().__init__(*args, **kwargs)

    def check_test_path(self, path: str):
        return self.repo_type in path and 'test' in path.lower()

    def check_test_filename(self, file_name: str):
        return self.repo_type in file_name and ('test_' in file_name.lower() or 'test' in file_name.lower())

    def analyze(self, repo_path, repo_type):

        repo_name = extractRepoName(repo_path)

        self.repo_type = '.' + repo_type
        if repo_name == "ansible" or repo_name == 'dbeaver':
            branch = 'devel'
        elif repo_name == 'home-assistant' or repo_name == 'HikariCP' or repo_name == 'TextBlob':
            branch = 'dev'
        elif repo_name == 'glances' or repo_name == 'androidannotations' or repo_name == 'zaproxy' or repo_name == 'fescar' or repo_name == 'boto':
            branch = 'develop'
        elif repo_name.lower() == 'rxjava' or repo_name == 'dex2jar':
            branch = '2.x'
        elif repo_name.lower() == 'exoplayer':
            branch = 'release-v2'
        elif repo_name == 'hadoop':
            branch = 'trunk'
        elif repo_name == 'mockito':
            branch = 'release/2.x'
        else:
            branch = 'master'
        if repo_name == 'netty':
            branch = '4.1'

        if repo_name == "vue":
            branch = "dev"
        elif repo_name == "two.js":
            branch = "dev"
        elif repo_name == "spine":
            branch = "dev"
        elif repo_name == "pixi.js":
            branch = "dev"
        elif repo_name == "Tone.js":
            branch = "dev"
        elif repo_name == "three.js":
            branch = "dev"
        elif repo_name == "basket.js":
            branch = "gh-pages"
        elif repo_name == "meteor":
            branch = "devel"
        elif repo_name == "hyper":
            branch = "canary"
        elif repo_name == "moment":
            branch = "develop"
        elif repo_name == "paper.js":
            branch = "develop"
        elif repo_name == "Rocket.Chat":
            branch = 'develop'
        elif repo_name == "select2":
            branch = "develop"
        elif repo_name == "storybook":
            branch = "next"
        elif repo_name == "element":
            branch = "dev"

        if repo_name == 'basket.js':
            branch = "gh-pages"
        if repo_name == "meteor":
            branch = "devel"
        if repo_name == "hyper":
            branch = "canary"
        if repo_name == "moment":
            branch = "develop"
        if repo_name == "paper.js":
            branch = "develop"
        if repo_name == "Rocket.Chat":
            branch = 'develop'
        if repo_name == "select2":
            branch = "develop"
        if repo_name == "storybook":
            branch = "next"
        if repo_name == "fabric":
            branch = "2.0"
        if repo_name == "powerline":
            branch = "develop"
        if repo_name == "salt":
            branch = "develop"
        if repo_name == "AiLearning":
            branch = "dev"
        if repo_name == "gensim":
            branch = "develop"
        if repo_name == "nltk":
            branch = "develop"
        if repo_name == "boto":
            branch = "develop"
        if repo_name == "TextBlob":
            branch = "dev"
        if repo_name == "pyinstaller":
            branch = "develop"
        if repo_name == "pyro":
            branch = "dev"
        if repo_name == 'vue':
            branch = 'dev'

        print(repo_name)
        self.repo = RepositoryMining('./repos/{}'.format(repo_name), only_in_branch=branch)

        i = 1
        for commit in self.repo.traverse_commits():
            if i > 10 or self.has_test:
                break
            self.analyze_commit(commit)
            i += 1

        file = open('./results/first10/{}/'.format(repo_type) + extractRepoName(repo_path) + '.json', 'w')
        file_out = {'has_test': self.has_test}
        file.write(json.dumps(file_out, indent=1))

        file.close()


    def analyze_commit(self, commit):
        for modification in commit.modifications:
            if not (self.repo_type in modification.filename):
                continue
            elif 'json' in modification.filename:
                continue
            else:
                if modification.new_path is not None:
                    path = modification.new_path

                elif modification.old_path is not None:
                    path = modification.old_path
                else:
                    print('what?')
                    exit(-1)

                if self.check_test_filename(modification.filename) or self.check_test_path(path):
                    self.has_test = True
                    return


def main():
    print('Working on javaScriptRepos')
    reposFile = open('javaScriptRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()

    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats2()
        repo_stats.analyze(repo, 'js')
        print("Done {}".format(repo))

    print("Working on python")
    reposFile = open('pythonrepolist.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()

    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats2()
        repo_stats.analyze(repo, 'py')
        print("Done {}".format(repo))

    print('Working on Java')
    reposFile = open('javaRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()
    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats2()
        repo_stats.analyze(repo, 'java')
        print("Done {}".format(repo))


    try:
        os.mkdir("./results/" + graphName)
    except:
        pass
    all_results = []
    for i in fileTypes:
        allFiles = os.listdir("./results/first10/" + i)
        total_files = 0
        has_tests = 0
        file_type_results = []
        for f in allFiles:
            fileName = f
            f = "./results/first10/" + i + "/" + f
            print(f)
            fp = open(f, "r")
            data = json.load(fp)
            fp.close()
            total_files += 1
            if data.get('has_test'):
                has_tests += 1
        outfile = './results/first10/{} summary.json'.format(i)
        outfile_fp = open(outfile, 'w')
        outfile_fp.write("tests in first 10 commits: {}\n Total repos: {}".format(has_tests, total_files))






main()
