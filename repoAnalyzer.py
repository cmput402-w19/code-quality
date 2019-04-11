from pydriller import RepositoryMining, GitRepository
import json
import os

# not using https://github.com/satwikkansal/wtfpython
# https://github.com/wangshub/wechat_jump_game
# https://github.com/sqlmapproject/sqlmap
# https://github.com/sivel/speedtest-cli
# https://github.com/mahmoud/awesome-python-applications
class RepoStats:
    def __init__(self, *args, **kwargs):
        self.commits_with_tests = 0
        self.total_commits = 0
        self.total_lines_net = 0
        self.test_lines_net = 0
        self.test_lines_per_commit = []
        self.total_lines_per_commit = []
        self.test_files = 0
        self.total_files = 0
        self.test_files_per_commit = []
        self.files_per_commit = []
        self.commits = {}
        self.actual_commits = 0
        self.repo = None
        return super().__init__(*args, **kwargs)

    def analyze(self, repo_path, repo_type):
        repo_name = extractRepoName(repo_path)
        if os.path.isfile('./results/{}/'.format(repo_type)+extractRepoName(repo_path)+'.json'):
            print("?")
            return
        self.repo_type = repo_type
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
        elif repo_name =="two.js":
            branch = "dev"
        elif repo_name =="spine":
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
        elif repo_name =="Rocket.Chat":
            branch = 'develop'
        elif repo_name == "select2":
            branch="develop"
        elif repo_name == "storybook":
            branch="next"
        elif repo_name == "element":
            branch="dev"

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
        if repo_name =="Rocket.Chat":
            branch = 'develop'
        if repo_name == "select2":
            branch="develop"
        if repo_name == "storybook":
            branch="next"
        if repo_name == "fabric":
            branch="2.0"
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


        self.repo = RepositoryMining('./repos/{}'.format(repo_name), only_in_branch=branch, only_modifications_with_file_types=[repo_type])
        file = open('./results/{}/'.format(repo_type)+extractRepoName(repo_path)+'.json', 'w')
        file.close()

        for commit in self.repo.traverse_commits():
            self.analyze_commit(commit)
            self.total_commits += 1
            if self.total_commits % 100 == 0:
                print("Working on commit {}".format(self.total_commits))
        self.actual_repo = GitRepository('./repos/{}'.format(repo_name))
        self.actual_commits = len(list(self.actual_repo.get_list_commits(branch=branch)))
        file_out = {
            'actual_commits': self.actual_commits,
            "commits_with_tests":self.commits_with_tests,
            "source_commits" : self.total_commits,
            "total_lines": self.total_lines_net,
            "test_lines": self.test_lines_net,
            "number_of_test_files": self.test_files,
            "number_of_total_files": self.total_files,
            "number_of_test_files_per_commit": self.test_files_per_commit,
            "number_of_files_per_commit": self.files_per_commit,
            'test_lines_per_commit': self.test_lines_per_commit,
            'total_lines_per_commit': self.total_lines_per_commit,
            'head_commit': self.actual_repo.get_head().hash
        }
        file = open('./results/{}/'.format(repo_type)+extractRepoName(repo_path)+'.json', 'w')
        file.write(json.dumps(file_out, indent=1))
        file.close()

    def check_test_path(self, path: str):
        return self.repo_type in path and ('test' in path or "Test" in path)

    def check_test_filename(self, file_name: str):
        return self.repo_type in file_name and ('test_' in file_name.lower() or 'test' in file_name.lower())


    def count_modification_stats(self,modification, commit):
        if self.commits.get(commit.hash) is None:
            self.commits[commit.hash] = True
            self.commits_with_tests += 1    # If a test file gets deleted, does this count as a commit with a test?
        # get test lines
        self.test_lines_net += modification.added - modification.removed

    # Function checks if a commit msg contains anything like "fix", "closes" or anything else that might indicate a bug fix that should have tests with it and returns True/False
    def check_if_commit_was_fix(self, commit):
        possibleMessages = ["fix", "closes", "fixes", "resolves"]
        for i in possibleMessages:
            if i in commit.msg:
                return True
        return False

    # Function checks if a commit has changed any test files
    def check_if_commit_has_test(self, commit):
        for modification in commit.modifications:
            if check_test_filename(modification):
                return True
            if check_test_path(modification):
                return True
        return False

    def analyze_commit(self, commit):
        test_lines_in_commit = 0
        total_lines_in_commit = 0
        delta_files_in_commit = 0
        delta_test_files_in_commit = 0

        for modification in commit.modifications:
            if modification.new_path is None and (self.check_test_path(modification.old_path) and self.check_test_filename(modification.filename)): # Deleted test file
                    self.count_modification_stats(modification, commit)
                    test_lines_in_commit += modification.added - modification.removed
                    delta_test_files_in_commit -= 1
                    total_lines_in_commit += modification.added - modification.removed
                    self.total_lines_net += modification.added - modification.removed

            elif modification.old_path is None and (self.check_test_path(modification.new_path) and self.check_test_filename(modification.filename)): # Added test file
                    self.count_modification_stats(modification, commit)
                    test_lines_in_commit += modification.added - modification.removed
                    delta_test_files_in_commit += 1
                    total_lines_in_commit += modification.added - modification.removed
                    self.total_lines_net += modification.added - modification.removed
            elif (modification.new_path is not None and self.check_test_path(modification.new_path) and self.check_test_filename(modification.filename)):
                self.count_modification_stats(modification, commit)
                test_lines_in_commit += modification.added - modification.removed
                total_lines_in_commit += modification.added - modification.removed
                self.total_lines_net += modification.added - modification.removed
            elif modification.old_path is not None and self.check_test_path(modification.old_path) and self.check_test_filename(modification.filename):
                self.count_modification_stats(modification, commit)
                test_lines_in_commit += modification.added - modification.removed
                total_lines_in_commit += modification.added - modification.removed
                self.total_lines_net += modification.added - modification.removed
            if modification.old_path is not None and self.repo_type in modification.old_path:
                total_lines_in_commit += modification.added - modification.removed
                self.total_lines_net += modification.added - modification.removed
            elif modification.new_path is not None and self.repo_type in modification.new_path:
                total_lines_in_commit += modification.added - modification.removed
                self.total_lines_net += modification.added - modification.removed
            if modification.old_path is None: # File added
                delta_files_in_commit += 1
            if modification.new_path is None: # File deleted
                delta_files_in_commit -= 1

            

        self.test_files += delta_test_files_in_commit
        self.total_files += delta_files_in_commit

        self.test_lines_per_commit.append(test_lines_in_commit)
        self.total_lines_per_commit.append(total_lines_in_commit)
        self.test_files_per_commit.append(delta_test_files_in_commit)
        self.files_per_commit.append(delta_files_in_commit)


def extractRepoName(url):
    url = url.split(".git")[0]
    url = url.split("/")[-1]
    return url


def main():

    print('Working on Java')
    reposFile = open('javaRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()
    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats()
        repo_stats.analyze(repo, '.java')
        print("Done {}".format(repo))



    print("Working on python")
    reposFile = open('pythonrepolist.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()

    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats()
        repo_stats.analyze(repo, '.py')
        print("Done {}".format(repo))

    print('Working on javaScriptRepos')
    reposFile = open('javaScriptRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:

        repoURLs.append(line)
    reposFile.close()
 
    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats()
        repo_stats.analyze(repo, '.js')
        print("Done {}".format(repo))
    return

main()
