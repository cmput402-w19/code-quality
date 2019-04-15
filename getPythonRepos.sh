cd repos
while read repo; do
    git clone "$repo"
done < ../pythonrepolist.txt
