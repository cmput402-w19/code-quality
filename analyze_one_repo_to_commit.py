from repoAnalyzer2 import RepoStats, extractRepoName


def main():
    repo_name = input("Please enter git url to the downloaded repo you wish to analyze: ").strip()
    repo_type = input("Plese enter the repo type (js, py, java): ")
    last_hash = input("Please enter the last commit you wish to analyze (Leave blank to analyze all commits): ").strip()
    last_hash = last_hash if last_hash != '' else None 
    stats = RepoStats()
    stats.analyze(repo_name, repo_type, last_hash)

if __name__ == '__main__':
    main()