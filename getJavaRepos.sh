cd repos
while read repo; do
    git clone "$repo"
done < ../javaRepos.txt