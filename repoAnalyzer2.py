from pydriller import RepositoryMining, GitRepository
from pydriller.domain.commit import ModificationType
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
        self.all_files = {}
        self.test_files_dict = {}
        self.fixes_with_tests = 0
        self.total_fixes = 0
        return super().__init__(*args, **kwargs)

    def analyze(self, repo_path, repo_type):

        repo_name = extractRepoName(repo_path)
        if os.path.isfile('./results/{}/'.format(repo_type) + extractRepoName(repo_path) + '.json'):
            print("?")
            return
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

        self.repo = RepositoryMining('./repos/{}'.format(repo_name), only_in_branch=branch,
                                     only_modifications_with_file_types=[self.repo_type])
        file = open('./results/{}/'.format(repo_type) + extractRepoName(repo_path) + '.json', 'w')
        file.close()

        for commit in self.repo.traverse_commits():
            self.analyze_commit(commit)
            self.total_commits += 1
            if self.total_commits % 10 == 0:
                print("Working on commit {}".format(self.total_commits))
        self.actual_repo = GitRepository('./repos/{}'.format(repo_name))
        self.actual_commits = len(list(self.actual_repo.get_list_commits(branch=branch)))
        def filter_list(x):
            return x > 0
        file_out = {
            'total_fixes': self.total_fixes,
            'fixes_with_tests': self.fixes_with_tests,
            'actual_commits': self.actual_commits,
            "commits_with_tests": self.commits_with_tests,
            "source_commits": self.total_commits,
            "total_lines": self.total_lines_net,
            "test_lines": self.test_lines_net,
            "number_of_test_files": len(list(filter(filter_list, list(self.all_files.values())))),
            "number_of_total_files": len(list(filter(filter_list, list(self.all_files.values())))),
            "number_of_test_files_per_commit": self.test_files_per_commit,
            "number_of_files_per_commit": self.files_per_commit,
            'test_lines_per_commit': self.test_lines_per_commit,
            'total_lines_per_commit': self.total_lines_per_commit,
            'head_commit': self.actual_repo.get_head().hash
        }

        file = open('./results/{}/'.format(repo_type) + extractRepoName(repo_path) + '.json', 'w')
        file.write(json.dumps(file_out, indent=1))
        file.close()

    def check_test_path(self, path: str):
        return self.repo_type in path and ('test' in path or "Test" in path)

    def check_test_filename(self, file_name: str):
        return self.repo_type in file_name and ('test_' in file_name.lower() or 'test' in file_name.lower())

    def count_modification_stats(self, path, diff, new_lines,commit):
        if self.commits.get(commit.hash) is None:
            self.commits[commit.hash] = True
            self.commits_with_tests += 1  # If a test file gets deleted, does this count as a commit with a test?
        # get test lines
        self.test_lines_net += diff
        self.test_files_dict[path] = new_lines

    def analyze_commit(self, commit):
        test_lines_in_commit = 0
        total_lines_in_commit = 0
        delta_files_in_commit = 0
        delta_test_files_in_commit = 0
        commit_fix = False
        has_test = False
        if self.check_if_commit_was_fix(commit):
            commit_fix = True
        for modification in commit.modifications:
            if not (self.repo_type in modification.filename and 'json' not in modification.filename):
                continue
            else:
                if modification.change_type == ModificationType.DELETE:
                    delta_files_in_commit -= 1
                    if self.check_test_filename(modification.filename) or self.check_test_path(modification.old_path):
                        delta_test_files_in_commit -= 1
                elif modification.change_type == ModificationType.ADD:
                    delta_files_in_commit += 1
                    if self.check_test_filename(modification.filename) or self.check_test_path(modification.new_path):
                        delta_test_files_in_commit += 1
                new_lines = modification.nloc if modification.nloc is not None else 0
                # Renaming of file... Arg
                if modification.change_type == ModificationType.RENAME:
                    self.all_files[modification.old_path] = 0
                    self.all_files[modification.new_path] = 0
                    path = modification.new_path
                    # Rename test file
                    if self.check_test_filename(modification.filename) or self.check_test_path(path):
                        self.test_files_dict[modification.old_path] = 0
                        self.test_files_dict[modification.new_path] = 0

                elif modification.new_path is not None:
                    path = modification.new_path
                    if self.check_test_filename(modification.filename) or self.check_test_path(path):
                        has_test = True
                elif modification.old_path is not None:
                    path = modification.old_path
                else:
                    print('what?')
                    exit(-1)

                if self.all_files.get(path) is None:
                    diff = new_lines
                    self.all_files[path] = diff

                    if self.check_test_filename(modification.filename) or self.check_test_path(path):
                        self.count_modification_stats(path, diff, new_lines, commit)
                        test_lines_in_commit += diff
                        has_test = True
                    if modification.change_type == ModificationType.DELETE:
                        self.all_files.pop(path)
                        if self.check_test_filename(modification.filename) or self.check_test_path(path):
                            self.test_files_dict.pop(path)

                else:
                    diff = new_lines - self.all_files[path]

                    self.all_files[path] = new_lines

                    if self.check_test_filename(modification.filename) or self.check_test_path(path):
                        self.count_modification_stats(path, diff, new_lines, commit)
                        test_lines_in_commit += diff
                        has_test = True
                    if modification.change_type == ModificationType.DELETE:
                        self.all_files.pop(path)
                        if self.check_test_filename(modification.filename) or self.check_test_path(path):
                            self.test_files_dict.pop(path)

                total_lines_in_commit += diff
        if commit_fix:
            if has_test:
                self.fixes_with_tests += 1
            self.total_fixes += 1
        self.test_files += delta_test_files_in_commit
        self.total_files += delta_files_in_commit
        self.total_lines_net += total_lines_in_commit
        self.test_lines_per_commit.append(test_lines_in_commit)
        self.total_lines_per_commit.append(total_lines_in_commit)
        self.test_files_per_commit.append(delta_test_files_in_commit)
        self.files_per_commit.append(delta_files_in_commit)


    def check_if_commit_was_fix(self, commit):
        possibleMessages = ["fix", "closes", "fixes", "resolves"]
        for i in possibleMessages:
            if i in commit.msg:
                return True
        return False


def extractRepoName(url):
    url = url.split(".git")[0]
    url = url.split("/")[-1]
    return url


def main():
    #repo = "https://github.com/encode/django-rest-framework.git"
    #repo = "https://github.com/codelucas/newspaper.git"
    #repo = 'https://github.com/coleifer/peewee.git'
    #repo_stats = RepoStats()
    #repo_stats.analyze(repo, 'python_test')
    print('Working on Java')
    reposFile = open('javaRepos.txt', 'r')
    repoURLs = []
    for line in reposFile:
        repoURLs.append(line)
    reposFile.close()
    for repo in repoURLs:
        print("Starting {}".format(repo))
        repo_stats = RepoStats()
        repo_stats.analyze(repo, 'java')
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
        repo_stats.analyze(repo, 'py')
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
        repo_stats.analyze(repo, 'js')
        print("Done {}".format(repo))
    return


main()
