import json
resultFile= open('./results/django.json')
results = json.load(resultFile)

print(sum(results['test_lines_per_commit']))
print(results['test_lines'])